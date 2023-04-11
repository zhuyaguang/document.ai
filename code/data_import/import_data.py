
import os
import tqdm
import openai

from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)

openai.api_key = "api-key"
openai.api_base =  "endpoint" # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2023-03-15-preview' # this may change in the future



def to_embeddings(items):
    response = openai.Embedding.create(
        input=items[1],
        engine="emb"
    )
    return [items[0], items[1], response["data"][0]["embedding"]]


if __name__ == '__main__':
    # 创建collection
    connections.connect("default", host="10.101.32.33", port="19530")
    fields = [
    FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="title", dtype=DataType.VARCHAR,max_length=200),
    FieldSchema(name="text", dtype=DataType.VARCHAR,max_length=200),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=1536)
]
    schema = CollectionSchema(fields, "hello_milvus is the simplest demo to introduce the APIs")
    hello_milvus = Collection("mydata", schema)


    count = 0


    for root, dirs, files in os.walk("./source_data"):
        for file in tqdm.tqdm(files):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.split('#####')
                    
                    item = to_embeddings(parts)
                    entities = [
                        [item[0]],  # field title
                        [item[1]],  # field text
                        [item[2]],  # field embeddings
                        ]
                    insert_result = hello_milvus.insert(entities)
            count += 1

    hello_milvus.flush()  
    index = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 128},
    }
    hello_milvus.create_index("embeddings", index)
    hello_milvus.load()
    