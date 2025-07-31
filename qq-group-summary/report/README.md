## OpenMCP News

Change when user update extension


## Context

You are a clever bot to write SPA page to display the changelog and news of my software OpenMCP.

### Some basic information you should know

- Release is: https://github.com/LSTM-Kirigaya/openmcp-client/releases
- OpenMCP website is: https://openmcp.kirigaya.cn/
- Github: https://github.com/LSTM-Kirigaya/openmcp-client
- Discord: https://discord.com/invite/SKTZRf6NzU
- QQ: https://qm.qq.com/cgi-bin/qm/qr?k=C6ZUTZvfqWoI12lWe7L93cWa1hUsuVT0&jump_from=webapi&authKey=McW6B1ogTPjPDrCyGttS890tMZGQ1KB3QLuG4aqVNRaYp4vlTSgf2c6dMcNjMuBD

### Design framework

You should obey the following order to make the page:

1. 📣 What is news in xxx
2. 🐳 Learn more features
3. ✨ Core Features
4. ❤️ How to sponsor
5. 📚 Resources
6. 🔧 Troubleshooting

### Some design requirements

- Theme color of openmcp is #B988D1, you should use it wisely and don't use light blue as default theme color, use #B988D1 instead.
- This is a website designed to be opened in vscode, so you should make vscode oriented design, where you should use following css macro to dev css class:
	```css
	:root {
		--font-monospace-family: var(--vscode-editor-font-family);
		--font-monospace-weight: var(--vscode-editor-font-weight);
		--font-monospace-size: var(--vscode-editor-font-size);
		
		--link-foreground: var(--vscode-textLink-foreground);
		--link-active: var(--vscode-textLink-activeForeground);

		/* UI & Control */
		--input-active-background: var(--vscode-input-background);
		--input-active-border: var(--vscode-focusBorder);
		--input-active-foreground: var(--vscode-input-foreground);

		--input-error-background: var(--vscode-inputValidation-errorBackground);
		--input-error-border: var(--vscode-inputValidation-errorBorder);
		--input-error-foreground: var(--vscode-inputValidation-errorForeground);

		--input-foreground: var(--vscode-input-foreground);
		--input-background: var(--vscode-input-background);
		--input-border: var(--vscode-input-border);
		--input-hover: var(--vscode-input-background);
		--input-placeholder: var(--vscode-input-placeholderForeground);
		--input-radius: 0px;

		--scrollbar-background: var(--vscode-scrollbarSlider-background);
		--scrollbar-hover: var(--vscode-scrollbarSlider-hoverBackground);
		--scrollbar-active: var(--vscode-scrollbarSlider-activeBackground);

		/* Window */
		--title-bar: #1f1f1f;
		--title-color: #fff;
		--foreground: var(--vscode-editor-foreground);
		--background: var(--vscode-editor-background);
		--label: rgb(189, 189, 189);
		--shadow: #000;
		--border: var(--vscode-input-border);
		--window-button-hover: rgba(255,255,255,0.1);
		--window-button-active: rgba(255,255,255,0.2);
		--window-blur-background: rgba(0,0,0,0.25);

		--window-title-foreground: var(--foreground);
		--window-background: var(--sidebar);
		--window-border: transparent;
		--window-radius: 0px;

		/* Sidebar */
		--sidebar: var(--vscode-sideBar-background);
		--sidebar-border: var(--vscode-sideBar-border);
		--sidebar-min-width: 280px;

		--sidebar-item-text: var(--vscode-list-inactiveSelectionForeground);
		--sidebar-item-border: var(--vscode-input-border);
		--sidebar-item-background: var(--sidebar);
		--sidebar-item-selected: var(--vscode-list-inactiveSelectionBackground);
		--sidebar-item-hover: var(--vscode-list-hoverBackground);
		--sidebar-item-max-height: 40px;
		--sidebar-item-radix-background: var(--vscode-breadcrumb-background);

		--sidebar-group-text: var(--vscode-sideBarSectionHeader-foreground);
		--sidebar-group-border: var(--vscode-sideBarSectionHeader-border);
		--sidebar-group-background: var(--vscode-sideBarSectionHeader-background);

		/* Labels */
		--signalSize-background: rgba(0,0,0,0.5);
		--signalSize-border: rgba(255,255,255,0.2);
		--signalSize-color: var(--foreground);

		/* Color Picker */
		--picker-swatch-size: 15px;
		--picker-swatch-cols: 8;
		--picker-background: var(--vscode-breadcrumbPicker-background);
		--picker-border: var(--vscode-dropdown-border);
		
		/* Search */
		--search-background: var(--vscode-quickInput-background);
		--search-border: var(--border);
		--search-panel-background: transparent;
		--search-panel-border: var(--vscode-pickerGroup-border);
		--search-panel-text: var(--vscode-quickInput-foreground);
		--search-label: var(--foreground);
		--search-selected-background: var(--vscode-list-inactiveSelectionBackground);

		/* Properties */
		--properties-background: var(--vscode-breadcrumb-background);
		--properties-border: var(--border);

		/* Navbar */
		--navBar-background: var(--sidebar);
		--navBar-height: 32px;
		--navBar-button: transparent;
		--navBar-button-text: var(--foreground);
		--navBar-group-background: var(--background);
		--navBar-preview-background: var(--vscode-scrollbarSlider-background);
		--navBar-slider-border: var(--foreground);

		/* Buttons */
		--button: var(--vscode-button-background);
		--button-text: var(--vscode-button-foreground);
		--button-hover: var(--vscode-button-hoverBackground);
		--button-active: var(--vscode-button-hoverBackground);
		--button-disabled: var(--vscode-activityBar-background);
		--button-disabled-text: var(--vscode-activityBar-inactiveForeground);

		/* Grid Lines */
		--grid-dash: 2;
		--grid-space: 4;
		--grid-line: var(--vscode-editorIndentGuide-background);
		--grid-tick: var(--vscode-editorIndentGuide-activeBackground);

		/* Cursor */
		--cursor: var(--vscode-editorCursor-foreground);
		--cursor-ghost: rgba(255, 255, 255, 0.2);
		--cursor-width: 2;

		/* X-Axis */
		--axis-height: 38px;
		--axis-line: var(--border);
		--axis-background: var(--vscode-sideBar-background);
		--axis-foreground: var(--foreground);

		/* Signals */
		--signal-highlight: var(--vscode-list-inactiveSelectionBackground);

		/* Colors */
		--accent: var(--vscode-button-background);
		--accent-dim: #234175;
		--accent-bright: #24c5f7;
		--accent-hover: var(--vscode-button-hoverBackground);

		--color-red: #ff5252;
		--color-pink: #ff4081;
		--color-purple: #e040fb;
		--color-deepPurple: #7c4dff;
		--color-indigo: #536dfe;
		--color-blue: #448aff;
		--color-lightBlue: #40c4ff;
		--color-cyan: #18ffff;
		--color-teal: #64ffda;
		--color-green: #69f0ae;
		--color-lightGreen: #b2ff59;
		--color-lime: #eeff41;
		--color-yellow: #ffff00;
		--color-amber: #ffd740;
		--color-orange: #ffab40;
		--color-deepOrange: #ff6e40;

		/* Settings */
		--settings-action-background: var(--background);
	}
	```