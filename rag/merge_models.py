import faiss

index_file_1 = "Math5_model.bin"
index_file_2 = "precalculus_model.bin"
merged_index_file = "Math_Model.bin"

index1 = faiss.read_index(index_file_1)
index2 = faiss.read_index(index_file_2)

if index1.d != index2.d:
    raise ValueError("The two FAISS indexes have different embedding dimensions and cannot be merged.")

index1.merge_from(index2)

faiss.write_index(index1, merged_index_file)

print(f"Merged FAISS index saved as {merged_index_file}")
