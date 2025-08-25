import json
import markdown

class File():

    """
    If we need to get text as markdown use type="markdown", type="text" use for send simple text
    """

    def __init__(self, doc_folder):
        self.doc_folder = doc_folder

    def write(filename : str, ctx : str, doc_folder : str, type = "text") -> None:
        file = open(doc_folder + "/" + filename, "w", encoding="utf-8")
        clear_str = []
        ctx = ctx.replace("    ", "")

        for i in ctx.split("\n"):
            if i != "":
                clear_str.append(i)

        JSON_file = {
            "filename" : filename,
            "type" : type,
            "dir" : doc_folder,
            "content" : "\n".join(clear_str)
        }

        file.write(json.dumps(JSON_file))
        file.close()

    def read(filename : str, doc_folder : str, type = "text") -> str:
        file = open(doc_folder + "/" +filename, "r", encoding="utf-8")
        ctx = file.read()
        file.close()

        JSON_file = json.loads(ctx)

        if type == "markdown":
            return markdown.markdown(JSON_file["content"])
        
        if type == "text":
            return JSON_file["content"]
        

    def file_architecture_check(filename : str, doc_folder : str) -> None:

        file = open(doc_folder + "/" +filename, "r", encoding="utf-8")
        ctx = file.read()

        try:
            JSON_file = json.loads(ctx)
            print(f"[SUCCESS] `{filename}` File use JSON")
            return None
        except:

            print(f"[ERROR] `{filename}` File don't use JSON")
            file = open(doc_folder + "/" + filename, "w", encoding="utf-8")

            JSON_file = {
                "filename" : filename,
                "type" : "text",
                "dir" : doc_folder,
                "content" : ctx
            }

            file.write(json.dumps(JSON_file))
            file.close()

            print(f"[SUCCESS] `{filename}` File was migrated on JSON")
            return None

