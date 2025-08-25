
editor.addEventListener('keyup', () => {
    console.log('Current text:', editor.innerHTML);
});

function sendText(ctx) {
    let text
    if (ctx === undefined) {
        text = document.getElementById("editor").innerText;
    } else {
        text = ctx
    }
    let filename = document.getElementById("filename").innerText;
    console.log(filename, text)
    fetch("/docs/edit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename: filename, text: text, action: "markdown-save" })
    })
    //.then(r => r.json())
    //.then(console.log)
    //.catch(console.error);

}

function showViewPage() {
    let main_block = document.getElementById("main-block")

    let text = document.getElementById("editor").innerText;
    let filename = document.getElementById("filename").innerText;
    
    console.log(filename, text)
    fetch("/docs/edit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename: filename, text: text, action: "markdown-view" })
    })
    .then(response => response.json())
    .then(r => {
        console.log(r);
        console.log(r["text"])
        main_block.innerHTML = `<div class="file">
            <div id="filename"> ${r["filename"]} </div>
            <div class="text">
                    ${r["text"]}
            </div>
            </div>
            
            <a href="/docs"><button id="send" onclick="sendText('${r["markdown"]}')">Save</button></a>`;
            
    })
    .catch(console.error);
}

