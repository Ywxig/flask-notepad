class File():

    def write(filename : str, ctx : str, doc_folder : str) -> None:
        file = open(doc_folder + "/" + filename, "w", encoding="utf-8")
        file.write(ctx)
        file.close()

    def read(filename : str, doc_folder : str) -> str:
        file = open(doc_folder + "/" +filename, "r", encoding="utf-8")
        ctx = file.read()
        file.close()
        return ctx
