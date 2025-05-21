const { handleToolCall } = require("./dist/index");

async function main() {
    const res = await handleToolCall(
        'k_navigate',
        {
            url: 'https://towardsdatascience.com/tag/editors-pick/'
        }
    )

    console.log(res);

    const res2 = await handleToolCall(
        'k_get_full_page_text'
    );

    console.log(res2);    
}

main();