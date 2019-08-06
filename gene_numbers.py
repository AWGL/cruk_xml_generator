

class GeneNumbers:

    def __init__(self, gene_name, panel, gene_num):
        self.valid_genes = [] #TODO Update this with a list of valid genes
        self.gene_name = gene_name
        self.panel = panel
        self.gene_num = gene_num


    def __repr__(self): #This is what the class appears as name of the object
        return self.gene_name


    def get_gene_name(self):
        return self.gene_name


    def get_panel(self):
        return self.panel


    def get_gene_num(self):
        return self.gene_num


    def isvalid(self):
        return self.gene_name in self.valid_genes