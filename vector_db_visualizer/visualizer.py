import pinecone
import numpy as np
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pinecone
from matplotlib.colors import LinearSegmentedColormap

pinecone.init(api_key='d8e80bbb-525e-475f-ac1c-4eae25c860bd', environment='gcp-starter')

import numpy as np
def get_ids_from_query(index, input_vector):
    print("searching pinecone...")
    results = index.query(vector=input_vector,
                          top_k=10000, include_values=False)
    ids = set()
    print(type(results))
    for result in results['matches']:
        ids.add(result['id'])
    return ids


def get_all_ids_from_index(index, num_dimensions, namespace=""):
    num_vectors = index.describe_index_stats(
    )["total_vector_count"]
    all_ids = set()
    while len(all_ids) < num_vectors:
        print("Length of ids list is shorter than the number of total vectors...")
        input_vector = np.random.rand(num_dimensions).tolist()
        print("creating random vector...")
        ids = get_ids_from_query(index, input_vector)
        print("getting ids from a vector query...")
        all_ids.update(ids)
        print("updating ids set...")
        print(f"Collected {len(all_ids)} ids out of {num_vectors}.")

    return all_ids

index = pinecone.Index("langchain1")
all_ids = get_all_ids_from_index(index, num_dimensions=1536, namespace="")
vectors = index.fetch(list(all_ids))
ids = []
embeddings = []
records = []

for id, vector in vectors['vectors'].items():
    record_id = int(vector["metadata"]["id"].replace("bookmark", ""))
    record_class = vector["metadata"]["class"]
    record_values = vector["values"]
    record = [record_id, record_class, record_values]
    records.append(record)

sorted_records = sorted(records, key=lambda x: x[0])



values = np.array([record[2] for record in sorted_records])

pca = PCA(n_components=3)
reduced_data = pca.fit_transform(values)

light_blue = (0.7, 0.85, 0.9)  
dark_blue = (0, 0.13, 0.25)   
colors = [light_blue, dark_blue]
n_bins = 100  
cmap_name = 'custom_blue_gradient'
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

num_records = len(sorted_records)

gradient_colors = [cm(i / (num_records - 1)) for i in range(num_records)]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(reduced_data[:, 0], reduced_data[:, 1], reduced_data[:, 2], c=gradient_colors)

sm = plt.cm.ScalarMappable(cmap=cm, norm=plt.Normalize(vmin=0, vmax=1))
sm.set_array([])  
cbar = plt.colorbar(sm, pad=0.1, ax=ax)
cbar.set_label('Position in Document (Light to Dark Blue)')

ax.set_xlabel('Component 1')
ax.set_ylabel('Component 2')
ax.set_zlabel('Component 3')

ax.set_title('3D Scatter Plot with Custom Blue Gradient')

plt.show()
