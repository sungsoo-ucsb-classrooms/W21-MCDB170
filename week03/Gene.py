class Gene():
    def __init__(self, gene_name, dna_seq_filename='', exon_position_filename='',   mRNA_seq_filename='', translation_conversion_map_filename=''):
        self.gene_name = gene_name
        self.dna_seq_filename = dna_seq_filename
        self.exon_position_filename = exon_position_filename
        self.mRNA_seq_filename = mRNA_seq_filename
        self.translation_conversion_map_filename = translation_conversion_map_filename
        
        self.dna_seq = ''
        self.exon_positions = []
        self.mRNA_seq = ''
        self.translation_conversion_map = {}
        self.protein_seq = ''
        
    def read_dna_seq_file(self, filename=''):
        if len(filename) == 0:
            filename = self.dna_seq_filename
        else:
            self.dna_seq_filename = filename
            
        lines = open(filename, 'r')
        self.dna_seq = ''.join([ line.strip() for line in lines ])
        
    def read_mRNA_seq_file(self, filename=''):
        if len(filename) == 0:
            filename = self.mRNA_seq_filename
        else:
            self.mRNA_seq_filename = filename
            
        lines = open(filename, 'r')
        self.mRNA_seq = ''.join([ line.strip() for line in lines ])
        
    def read_exon_positions(self, filename=''):
        if len(filename) == 0:
            filename = self.exon_position_filename
        else:
            self.exon_postion_filename = filename
            
        self.exon_positions = [  tuple(int(num_str) for num_str in line.split() )  for line in open(filename,'r') ]

    def create_mRNA(self):
        self.mRNA_seq = ''
        for begin, end in self.exon_positions:
            self.mRNA_seq += self.dna_seq[begin:end].replace('T','U')

    def save_mRNA_seq(self, filename='', letters_per_line = 70):
        if len(filename) == 0:
            filename = self.mRNA_seq_filename
        else:
            self.mRNA_seq_filename = filename
            
        savefile = open(filename, 'w')
        for i in range(0, len(self.mRNA_seq), letters_per_line):
            begin = i
            end = begin + letters_per_line
            savefile.write(self.mRNA_seq[begin:end] + '\n')
        savefile.close()
        
    def read_translation_conversion_map(self, filename=''):
        if len(filename) == 0:
            filename = self.translation_conversion_map_filename 
        else:
            self.translation_conversion_map_filename = filename
            
        self.translation_conversion_map = { line.split()[0]:line.split()[1:]  for line in open(filename, 'r') }
    
    def create_protein_seq(self):
        self.protein_seq = ''
        begin_pos = self.mRNA_seq.find('AUG')

        for i in range(begin_pos, len(self.mRNA_seq), 3):
            triplet = self.mRNA_seq[i:i+3]
            amino_acid = self.translation_conversion_map[triplet][0]
            if amino_acid == 'X':
                break;
            else:
                self.protein_seq += amino_acid
