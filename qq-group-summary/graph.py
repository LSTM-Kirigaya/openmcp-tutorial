# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.font_manager import FontProperties
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.colors import to_rgba
import matplotlib.patheffects as path_effects
from PIL import Image
import requests
from io import BytesIO
import os
import warnings
import numpy as np

# try cairosvg for svg -> png conversion if available
try:
    import cairosvg
except Exception:
    cairosvg = None

# -------------------------
# 配置
# -------------------------
CHAT_JSON = "report/src/summarize_chat.json"
USER_JSON = "report/src/summarize_user.json"
FAVICON_PATH = "report/public/favicon.png"
QR_PATH = "report/public/openmcp-qq-group.png"

THEME_COLOR = "#B988D1"
TOPIC_COLOR = "#f2f0f5"
EDGE_COLOR = "#A88AC0"
MAX_SCALE = 1.35
FIGSIZE = (14, 10)
DPI = 200
IMG_H_FRAC = 0.1


# -------------------------
# 中文字体加载
# -------------------------
def find_good_chinese_font():
    candidates = [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Supplemental/STHeiti Medium.ttc",
        "/System/Library/Fonts/Supplemental/PingFang.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttf",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]
    from matplotlib.ft2font import FT2Font
    for p in candidates:
        if p and os.path.exists(p):
            try:
                FT2Font(p)
                return p
            except Exception:
                continue
    import matplotlib.font_manager as fm
    sys_fonts = fm.findSystemFonts()
    keywords = ["noto", "source", "cjk", "pingfang", "hei", "yahei", "wqy", "song"]
    for fp in sys_fonts:
        name = os.path.basename(fp).lower()
        if any(k in name for k in keywords):
            try:
                FT2Font(fp)
                return fp
            except Exception:
                continue
    return None


def export_to_relation_graph(output_path: str) -> str:

    font_path = find_good_chinese_font()
    if font_path:
        zh_font = FontProperties(fname=font_path)
    else:
        zh_font = FontProperties()
        warnings.warn("未找到可靠中文字体，中文可能无法正确渲染。")

    # -------------------------
    # 读取 JSON
    # -------------------------
    with open(CHAT_JSON, 'r', encoding='utf-8') as f:
        chat = json.load(f)
    with open(USER_JSON, 'r', encoding='utf-8') as f:
        users = json.load(f)

    # 收集 contributors
    contributors_set = set()
    for m in chat.get("messages", []):
        for c in m.get("contributors", []):
            if isinstance(c, str):
                contributors_set.add(c.strip())

    # 用户 meta 映射
    user_meta = {t.get("name"): t for t in users.get("titles", []) if t.get("name")}

    # -------------------------
    # 构建有向图：user -> topic
    # -------------------------
    G = nx.DiGraph()
    for m in chat.get("messages", []):
        topic = m.get("topic")
        topic_node = f"topic: {topic}"
        G.add_node(topic_node, type="topic", label=topic)
        for c in m.get("contributors", []):
            name = c.strip()
            if not G.has_node(name):
                G.add_node(name, type="user")
            G.add_edge(name, topic_node)

    user_nodes = [n for n, d in G.nodes(data=True) if d.get("type") == "user"]
    if not user_nodes:
        raise RuntimeError("未在 chat 中发现任何 contributors，请检查 JSON 文件")

    # -------------------------
    # 入度映射头像大小
    # -------------------------
    in_degrees = {u: G.in_degree(u) for u in user_nodes}
    min_deg = min(in_degrees.values())
    max_deg = max(in_degrees.values())
    base_area = 1200
    node_size_map = {}
    for u, deg in in_degrees.items():
        if max_deg == min_deg:
            node_size_map[u] = base_area
        else:
            t = (deg - min_deg) / (max_deg - min_deg)
            radius_scale = 1.0 + t * (MAX_SCALE - 1.0)
            node_size_map[u] = base_area * (radius_scale ** 2)

    topic_area = 2000

    # -------------------------
    # 绘图
    # -------------------------
    fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
    fig.patch.set_facecolor("#24272D")
    ax = fig.add_subplot(1,1,1)
    ax.axis('off')

    pos = nx.spring_layout(G, k=1.5, seed=42, iterations=200)


    # 绘制话题节点 - 调整样式
    topic_nodes = [n for n,d in G.nodes(data=True) if d.get("type")=="topic"]
    nx.draw_networkx_nodes(G, pos, nodelist=topic_nodes, node_size=topic_area,
                        node_color="#3A2C40", linewidths=1.5,  # 更深的紫色
                        edgecolors='#B988D1', alpha=0.9, ax=ax)  # 使用主题色作为边框

    # 绘制话题标签
    for n in topic_nodes:
        x,y = pos[n]
        ax.text(x,y,G.nodes[n]['label'], fontsize=13, fontproperties=zh_font,
                ha='center', va='center', color="#B988D1",
                path_effects=[path_effects.Stroke(linewidth=2.2, foreground="#2b1b2b", alpha=0.6),
                            path_effects.Normal()],
                            zorder=22)

    # -------------------------
    # 用户头像 + QQ ID
    # -------------------------
    import os
    from pathlib import Path
    from PIL import ImageDraw

    def create_circular_mask(size):
        """创建圆形遮罩"""
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        return mask

    def crop_to_circle(img):
        """将图像裁剪为圆形"""
        # 确保图像是正方形
        width, height = img.size
        min_dim = min(width, height)
        
        # 居中裁剪为正方形
        left = int((width - min_dim) / 2)
        top = int((height - min_dim) / 2)
        right = left + min_dim
        bottom = top + min_dim
        img = img.crop((left, top, right, bottom))
        
        # 创建与图像相同大小的遮罩
        mask = create_circular_mask((min_dim, min_dim))
        
        # 确保图像和遮罩都是RGBA模式
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 应用圆形遮罩
        img.putalpha(mask)
        return img

    # 创建缓存文件夹
    cache_dir = Path("avatars")
    cache_dir.mkdir(exist_ok=True)

    for u in user_nodes:
        x, y = pos[u]
        meta = user_meta.get(u, {})
        qq = meta.get("qq")
        
        # 计算节点半径（用于确定头像大小）
        node_radius = np.sqrt(node_size_map[u] / np.pi)
        avatar_size = int(node_radius * 2)  # 头像大小为节点直径的80%
        
        if qq:
            # 缓存文件路径
            cache_file = cache_dir / f"{qq}.png"
            img_success = False
            
            url = f"https://q1.qlogo.cn/g?b=qq&nk={qq}&s=640"
            try:
                resp = requests.get(url, timeout=5)
                resp.raise_for_status()
                
                # 保存到缓存
                with open(cache_file, 'wb') as f:
                    f.write(resp.content)
                
                img = Image.open(BytesIO(resp.content)).convert("RGBA")
                img_success = True
                print(f"下载并缓存头像: {qq}")
            except Exception as e:
                print(f"下载头像失败 {qq}: {e}")
            
            # 如果成功获取头像
            if img_success:
                # 裁剪为圆形
                img = crop_to_circle(img)
                
                # 调整头像大小以匹配节点大小
                zoom_factor = avatar_size / max(img.size)
                
                ab = AnnotationBbox(OffsetImage(img, zoom=zoom_factor), (x,y), frameon=False, zorder=20)
                ax.add_artist(ab)
                
                text_offset = 1 * zoom_factor
                
                # QQ ID
                ax.text(x, y - text_offset, u, fontsize=9, fontproperties=zh_font,
                        ha='center', va='top', color='#F9F9F9',
                        path_effects=[path_effects.Stroke(linewidth=1, foreground=THEME_COLOR, alpha=0.6),
                                    path_effects.Normal()], zorder=25)
            else:
                # 头像获取失败，使用默认样式
                ax.scatter(x, y, s=node_size_map[u], c=THEME_COLOR, edgecolors="#6a3f7a", 
                        linewidths=1.5, zorder=15, alpha=0.9)
                ax.text(x, y, u, fontsize=9, fontproperties=zh_font,
                        ha='center', va='center', color='white', zorder=20)
        else:
            # 没有QQ号，使用默认样式
            ax.scatter(x, y, s=node_size_map[u], c=THEME_COLOR, edgecolors="#6a3f7a", 
                    linewidths=1.5, zorder=15, alpha=0.9)
            ax.text(x, y, u, fontsize=9, fontproperties=zh_font,
                    ha='center', va='center', color='white', zorder=20)


    # 绘制边
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(),
                        arrowstyle='-|>', arrowsize=12, width=1.2,
                        edge_color=EDGE_COLOR, alpha=0.9,
                        connectionstyle='arc3,rad=0.08', ax=ax,
                            min_target_margin=2000, min_source_margin=2000)


    fav_img = Image.open(FAVICON_PATH).convert("RGBA")
    qr_img = Image.open(QR_PATH).convert("RGBA")
    pad = 0.02
    gap = 0.01
    fig_w, fig_h = FIGSIZE
    current_x = 1.0 - pad

    def img_width_frac(img, img_h_frac):
        if img is None:
            return 0.0
        w,h = img.size
        return img_h_frac * (fig_h/fig_w) * (w/h)

    # favicon
    if fav_img:
        fav_w_frac = img_width_frac(fav_img, IMG_H_FRAC)
        left = current_x - fav_w_frac
        left = max(left, pad)
        ax_fav = fig.add_axes([left, pad, fav_w_frac, IMG_H_FRAC], zorder=40)
        ax_fav.imshow(fav_img)
        ax_fav.axis('off')
        current_x = left - gap

    # qr
    if qr_img:
        qr_w_frac = img_width_frac(qr_img, IMG_H_FRAC)
        left = max(pad, current_x - qr_w_frac)
        ax_qr = fig.add_axes([left, pad, qr_w_frac, IMG_H_FRAC], zorder=40)
        ax_qr.imshow(qr_img)
        ax_qr.axis('off')
        current_x = left - gap

    # 文字
    credit_txt = "由锦恢呈现"
    copyright_txt = "LSTM-Kirigaya/openmcp-tutorial © 锦恢"
    fig.text(current_x, pad+IMG_H_FRAC*0.65, credit_txt, ha='right', va='center',
            fontproperties=zh_font, fontsize=15, color="#D5D5D5", zorder=50)
    fig.text(current_x, pad+IMG_H_FRAC*0.25, copyright_txt, ha='right', va='center',
            fontproperties=zh_font, fontsize=10, color="#9A9A9A", zorder=50)

    # -------------------------
    # 保存 PNG
    # -------------------------
    plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
    fig.savefig(output_path, dpi=DPI, bbox_inches='tight', pad_inches=0.2)
    plt.close(fig)

    return output_path

if __name__ == '__main__':
    export_to_relation_graph('hello.png')