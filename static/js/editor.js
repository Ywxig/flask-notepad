
function insert(prefix = true, ctx) {
    const textarea = document.getElementById("textarea");
    if (prefix === true) {
        textarea.value += `\n\n${ctx}`;
    } else {
         textarea.value += `${ctx}`;
    }
    
    return
}