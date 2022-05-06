f = open('source_holder.txt')  
data = f.readlines()
f.truncate()

print(data)