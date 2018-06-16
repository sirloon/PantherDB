import re
import os.path 

def load_data (data_folder):
         
         data_file = os.path.join(data_folder, "Testfile_PantherDB.txt") 
         
         # this empty dictionary is for storing the final output 
         d = {}
         # this empty list is for storing the orthologs of the same reference gene
         o = []
         # this empty list stores the common Uniprot_ID temporarily for comparison 
         e = None 
     
         # Define a function that takes the datafile as the sole argument               
         with open(data_file, "r+") as f:# change this to the file name
             # This function is for splitting the line
             for line in f:
                 y = re.split("[\| \t \n]", line)
                 z = re.split("=", y [2])
                 a = re.split("=", y [1])
                 b = re.split("=", y [4])
                 c = re.split("=", y [5])
                 # The above are only intermediates
                 # The below are the important variables
                 ref_gene_uniprot_id = z [1]
                 ref_gene_db_name = a [0]
                 ref_gene_db_id = a[-1]
                 ortholog_db_name = b [0]
                 ortholog_db_id = b [-1]
                 ortholog_uniprot_id = c [1]
                 ortholog_type = y [6]
                 ortholog_family = y [8]
        
                 if e is None: # for the first item
                    e = ref_gene_uniprot_id
                    d = { "id": ref_gene_uniprot_id,
                           "pantherdb": {
                           ref_gene_db_name: ref_gene_db_id,
                           "uniprot_kb": ref_gene_uniprot_id,
                           }
                        }
           
                 if ref_gene_uniprot_id != e: # if read up to a different ref. gene 
                      d = { "id": ref_gene_uniprot_id,
                            "pantherdb": {
                            ref_gene_db_name: ref_gene_db_id,
                            "uniprot_kb": ref_gene_uniprot_id,
                            "orthologs" : o
                            }
                          }
                      yield d  
                      d.clear()
                      e = ref_gene_uniprot_id
                      d = { "id": ref_gene_uniprot_id,
                            "pantherdb": {
                            ref_gene_db_name: ref_gene_db_id,
                            "uniprot_kb": ref_gene_uniprot_id
                            }
                          }
                      o = [{ortholog_db_name: ortholog_db_id,
                             "uniprot_kb": ortholog_uniprot_id,
                             "ortholog_type": ortholog_type,
                             "panther_family": ortholog_family
                             }
                          ]
        
                 else: # in this case the ref. gene is the same, just append the ortholog 
                     new = {ortholog_db_name: ortholog_db_id,
                            "uniprot_kb": ortholog_uniprot_id,
                            "ortholog_type": ortholog_type,
                            "panther_family": ortholog_family
                            }
                     o.append(new)
              
             if o:
             # at the last item, the ortholog is created but since it has no next ref_gene_uniprot_id to compare,
             # it does not go to the second if and output the result
             # and thus we need to let it output the result by giving it the condition if o == true. 
                d = d = { "id": ref_gene_uniprot_id,
                            "pantherdb": {
                            ref_gene_db_name: ref_gene_db_id,
                            "uniprot_kb": ref_gene_uniprot_id,
                            "orthologs" : o
                            }
                          }
                yield d       
       
if "__name__" == "__main__":
	g = load_data(data_folder)
