import re

splits = {"train":"split/train.txt","test":"split/test.txt","devel":"split/devel.txt"}
dir_to_standoff = "standoff/"

species = {};

for split_name in ["train", "test", "devel"]:
  file1 = open("conll2/"+split_name+".tsv", "w")  
  a_file = open(splits[split_name])
  for filename_begin in a_file.readlines()[0:2]:
    a_txt_file = open(dir_to_standoff+filename_begin.strip()+".txt")
    an_ann_file = open(dir_to_standoff+filename_begin.strip()+".ann")
    file_content = a_txt_file.read()
    species_for_ann_file = []
    
    for ann_iter in an_ann_file.readlines():
      species_match = re.search("Species (\d+) (\d+)", ann_iter, flags = 0) 
      if species_match != None:
        #print(ann_iter)
        species_match_begin = int(species_match.group(1)) 
        species_match_end = int(species_match.group(2)) 
        species_for_ann_file.append((species_match_begin,species_match_end))
        
    #print(file_content)
    spl = re.split('(\W)', file_content)
    total = 0 
    lengths = [total]

    for elem in map(lambda x:len(x), spl):
      total += elem
      lengths.append(total)

    #for elem,ind in zip(spl,range(0,len(spl))):
    #  print(elem+"\t"+str(ind))

    labels = []
    for i in lengths:
      labels.append('O')

    #print(lengths)
    #print(labels)
    #print(spl)

    #for i in range(36,43):
    #  print(spl[i])

    start = 0
    for species in species_for_ann_file:
      indBegin = lengths.index(species[0])#,start)
      indEnd = lengths.index(species[1])#,start + indBegin)
      #print(indBegin,indEnd)
      for i in range(indBegin,indEnd):
        if i == indBegin:
          labels[i] = "B-Species"
        else:
          labels[i] = "I-Species"      
      start = indEnd

    #content = ""

    for i,elem, label in zip(range(0,len(spl)),spl,labels):
      if elem != "\n" and elem != '' and elem != " ":
        #print(elem+"\t"+label)
        file1.write(elem+"\t"+label+"\n")
      #if label != 'O':
      #  print(str(i)+"\t"+elem+"\t\t\t"+label)

    file1.write("\n")
    #  print(line)
    
    a_txt_file.close()
    an_ann_file.close()

  a_file.close()

file1.close()

