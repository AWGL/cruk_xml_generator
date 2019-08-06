import csv
from gene_numbers import GeneNumbers

class ImportGenesNumbers:

    def __init__(self, file_location):
        self.file_location = file_location


    def load_csv(self):
        csv_dict = {}
        with open(self.file_location, 'r') as csv_file:
            genes_data = csv.reader(csv_file)
            headers = next(genes_data, None) # Skip the headers
            for gene_data in genes_data:
                gene = GeneNumbers(gene_data[0], gene_data[1], gene_data[2])
                csv_dict[gene.get_gene_name()] = gene
        return csv_dict


'''
def main():
    genes_numbers = load_csv(os.path.join(input_path, input_file_name))
    print(genes_numbers)
    print(genes_numbers.get("AKT1").get_gene_num()) # how to use the data inside the class


if __name__ == '__main__':
    main()
'''