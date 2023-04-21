.. code:: ipython3

    import pandas as pd
    import json
    import requests
    import re
    from bs4 import BeautifulSoup
    # load the JSON file as a dictionary
    with open('tmpsb1s7uuv.json', 'r') as f:
        data = json.load(f)
    data = pd.json_normalize(data)
    # convert the dictionary to a dataframe
    df = pd.DataFrame.from_dict(data)
    df = pd.concat([df.drop('collections', axis=1),
                    pd.json_normalize(df['collections']).add_prefix('collect.')], axis=1)
    df = df.dropna(subset = ['collect.0'])
    df['area'] = df['collect.0'].apply(lambda x: x.get('area'))
    df['collections'] = df['collect.0'].apply(lambda x: x.get('collection'))
    pattern = r'Componenttype.*?Categories'
    df['components'] = df['url'].apply(lambda x: boringfunc(x))
    


.. code:: ipython3

    import pandas as pd
    import json
    import requests
    import re
    from bs4 import BeautifulSoup
    general = BeautifulSoup(requests.get('https://paperswithcode.com/methods/area/general').content, 'html.parser')
    a_tags = general.find_all('a', href=lambda href: href and href.startswith('/methods/category/'))
    category = []
    for a_tag in a_tags:
        href = a_tag['href']
        text = a_tag.text
        index_see = text.find("See")
        category.append(text)

.. code:: ipython3

    def boringfunc(x):
        types = []
        soup = BeautifulSoup(requests.get(x).content, 'html.parser')
        spans = soup.find_all('span', class_='badge badge-primary')
        for span in spans:
            text = span.get_text().replace('\n','').lower()
            types.append(text)
        return list(set(types))

.. code:: ipython3

    boringfunc('https://paperswithcode.com/method/resnet')

.. code:: ipython3

    for i in range(len(category)-1, -1, -1):
        if i % 2 != 0:
            del category[i]


.. code:: ipython3

    general
    capital_words = re.findall(r'\b[A-Z][a-z]*\b', general)

.. code:: ipython3

    capital_words = [x for x in capital_words if x not in ["See",'General']]

.. code:: ipython3

    capital_words

.. code:: ipython3

    import pandas as pd
    import numpy as np
    import re
    df = pd.read_csv('webscraped1.csv')
    pattern = r'Componenttype.*?Categories'

.. code:: ipython3

    df[df['components'] == "['absolute position encodings', 'scaled dot-product attention', 'dense connections', 'residual connection', 'spatial-reduction attention', 'layer normalization', 'vision transformers']"]

.. code:: ipython3

    for i in range(0,df.shape[0]):
        if '🤖' in df['components'].at[i]:
            df['components'].at[i] = np.nan

.. code:: ipython3

    sum(df['components'].isna())

.. code:: ipython3

    df['components'] = df['components'].apply(lambda x: re.search(pattern, x, flags=re.IGNORECASE).group(0) if re.search(pattern, x, flags=re.IGNORECASE) else x)

.. code:: ipython3

    df['components'] = df['components'].apply(lambda x: x.replace('\n',''))


.. code:: ipython3

    df['components'] = df['components'].apply(lambda x: " ".join(x.split()))

.. code:: ipython3

    df[['area','components']].to_csv('webscraped1.csv', index=False)

.. code:: ipython3

    df['area'].unique()

.. code:: ipython3

    df = df.dropna(subset = ['components'])

.. code:: ipython3

    df['components'] = df['components'].apply(lambda x :x.split()[4:-1])

.. code:: ipython3

    a = []
    for i in df.groupby('area').groups:
        a.append(df.groupby('area').get_group(i))

.. code:: ipython3

    a[0]

.. code:: ipython3

    # # convert the dataframe to a string and remove whitespace characters
    # df_string = a[0].to_string(header=False, index=False).replace('\n', '').replace(' ', '')
    
    # write the string to a text file
    with open('outputaudio.txt', 'w') as file:
        for index, row in a[0].iterrows():
            row_string = row.values[1].replace('[', '').replace(']', '').replace("'", '')
            file.write(row_string + '\n')

.. code:: ipython3

    with open('outputcv.txt', 'w') as file:
        for index, row in a[1].iterrows():
            row_string = row.values[1].replace('[', '').replace(']', '').replace("'", '')
            file.write(row_string + '\n')

.. code:: ipython3

    with open('outputgeneral.txt', 'w') as file:
        for index, row in a[2].iterrows():
            row_string = row.values[1].replace('[', '').replace(']', '').replace("'", '')
            file.write(row_string + '\n')

.. code:: ipython3

    with open('outputgraphs.txt', 'w') as file:
        for index, row in a[3].iterrows():
            row_string = row.values[1].replace('[', '').replace(']', '').replace("'", '')
            file.write(row_string + '\n')

.. code:: ipython3

    with open('outputNLP.txt', 'w') as file:
        for index, row in a[4].iterrows():
            row_string = row.values[1].replace('[', '').replace(']', '').replace("'", '')
            file.write(row_string + '\n')

.. code:: ipython3

    with open('outputRL.txt', 'w') as file:
        for index, row in a[5].iterrows():
            row_string = row.values[1].replace('[', '').replace(']', '').replace("'", '')
            file.write(row_string + '\n')

.. code:: ipython3

    with open('outputsqe.txt', 'w') as file:
        for index, row in a[6].iterrows():
            row_string = row.values[1].replace('[', '').replace(']', '').replace("'", '')
            file.write(row_string + '\n')

.. code:: ipython3

    def hash_string(s):
        # initialize the hash value to a prime number
        try:
            if type(int(s)) == int:
                return s
        except ValueError:
            hash_value = 17
        
            # iterate through each character in the string
            for c in s:
                # update the hash value with the ASCII value of the character
                hash_value = (hash_value * 31 + ord(c)) % 1000000007
        
            return hash_value
    def read_transactions1(file_name):
        """
        Reads transaction data from a file and returns a list of sets, where each set
        represents a transaction and contains the items in the transaction.
        """
        with open(file_name, 'r') as f:
            transactions = []
            for line in f:
                items = line.strip().split(', ')
                dic = {}
                for item in items:
                    dic[item] = hash_string(item)
                transactions.append(dic)
            return transactions

.. code:: ipython3

    a = read_transactions1('outputaudio.txt')
    b = read_transactions1('outputcv.txt')
    c = read_transactions1('outputgeneral.txt')
    d = read_transactions1('outputgraphs.txt')
    e = read_transactions1('outputNLP.txt')
    f = read_transactions1('outputRL.txt')
    g = read_transactions1('outputsqe.txt')

.. code:: ipython3

    a = {value: key for d in a for key, value in d.items()}
    b = {value: key for d in b for key, value in d.items()}
    c = {value: key for d in c for key, value in d.items()}
    d = {value: key for i in d for key, value in i.items()}
    e = {value: key for d in e for key, value in d.items()}
    f = {value: key for d in f for key, value in d.items()}
    g = {value: key for d in g for key, value in d.items()}


.. code:: ipython3

    with open('outputaudio1.txt', 'w') as file:
        a = read_transactions1('outputaudio.txt')
        for row in a:
            for item,value in row.items():
                row_string = value
                file.write(str(row_string) + ' ')
            file.write('\n')

.. code:: ipython3

    with open('outputcv1.txt', 'w') as file:
        a = read_transactions1('outputcv.txt')
        for row in a:
            for item,value in row.items():
                row_string = value
                file.write(str(row_string) + ' ')
            file.write('\n')

.. code:: ipython3

    with open('outputgeneral1.txt', 'w') as file:
        a = read_transactions1('outputgeneral.txt')
        for row in a:
            for item,value in row.items():
                row_string = value
                file.write(str(row_string) + ' ')
            file.write('\n')

.. code:: ipython3

    with open('outputgraphs1.txt', 'w') as file:
        a = read_transactions1('outputgraphs.txt')
        for row in a:
            for item,value in row.items():
                row_string = value
                file.write(str(row_string) + ' ')
            file.write('\n')

.. code:: ipython3

    with open('outputNLP1.txt', 'w') as file:
        a = read_transactions1('outputNLP.txt')
        for row in a:
            for item,value in row.items():
                row_string = value
                file.write(str(row_string) + ' ')
            file.write('\n')

.. code:: ipython3

    with open('outputRL1.txt', 'w') as file:
        a = read_transactions1('outputRL.txt')
        for row in a:
            for item,value in row.items():
                row_string = value
                file.write(str(row_string) + ' ')
            file.write('\n')

.. code:: ipython3

    with open('outputsqe1.txt', 'w') as file:
        a = read_transactions1('outputsqe.txt')
        for row in a:
            for item,value in row.items():
                row_string = value
                file.write(str(row_string) + ' ')
            file.write('\n')

.. code:: ipython3

    hash_string('convolution')

.. code:: ipython3

    df['components']

.. code:: ipython3

    import itertools
    def read_transactions(file_name):
        """
        Reads transaction data from a file and returns a list of sets, where each set
        represents a transaction and contains the items in the transaction.
        """
        with open(file_name, 'r') as f:
            transactions = []
            for line in f:
                items = line.strip().split(',')
                transactions.append(set(items))
            return transactions
    
    def get_frequent_itemsets(transactions, min_support):
        """
        Returns the frequent itemsets in the given transactions that have a support greater
        than or equal to the given minimum support, using the Apriori algorithm.
        """
        # Compute the frequent 1-itemsets
        freq_itemsets = []
        item_counts = {}
        for transaction in transactions:
            for item in transaction:
                item_counts[item] = item_counts.get(item, 0) + 1
        for item, count in item_counts.items():
            if count >= min_support:
                freq_itemsets.append(frozenset([item]))
        
        # Iteratively generate larger frequent itemsets until no more can be found
        k = 2
        while True:
            # Generate candidate itemsets
            candidate_itemsets = set()
            for i, itemset1 in enumerate(freq_itemsets):
                for itemset2 in freq_itemsets[i+1:]:
                    candidate_itemset = itemset1.union(itemset2)
                    if len(candidate_itemset) == k and candidate_itemset not in candidate_itemsets:
                        candidate_itemsets.add(candidate_itemset)
            
            # Count support of candidate itemsets
            item_counts = {}
            for transaction in transactions:
                for candidate_itemset in candidate_itemsets:
                    if candidate_itemset.issubset(transaction):
                        item_counts[candidate_itemset] = item_counts.get(candidate_itemset, 0) + 1
            
            # Check if any frequent itemsets were found
            if not item_counts:
                break
            
            # Filter candidate itemsets that don't meet the minimum support threshold
            freq_itemsets = [itemset for itemset, count in item_counts.items() if count >= min_support]
            
            # If no frequent itemsets were found, stop searching
            if not freq_itemsets:
                break
            
            k += 1
        return freq_itemsets

.. code:: ipython3

    def generate_association_rules(freq_itemsets, transactions, min_conf):
        """
        Generates association rules for the given frequent itemsets that have a confidence
        greater than or equal to the given minimum confidence.
        """
        # Convert transactions to a list of sets
        item_sets = [set(transaction) for transaction in transactions]
        
        # Generate association rules
        association_rules = []
        for itemset in freq_itemsets:
            if len(itemset) > 1:
                for i in range(1, len(itemset)):
                    for antecedent in itertools.combinations(itemset, i):
                        antecedent = frozenset(antecedent)
                        consequent = itemset.difference(antecedent)
                        antecedent_support = sum([1 for item_set in item_sets if antecedent.issubset(item_set)])
                        consequent_support = sum([1 for item_set in item_sets if consequent.issubset(item_set)])
                        support = (antecedent_support + consequent_support) / len(item_sets)
                        confidence = antecedent_support / len([item_set for item_set in item_sets if antecedent.issubset(item_set)])
                        lift = confidence / (consequent_support / len(item_sets))
                        if confidence >= min_conf:
                            association_rules.append((antecedent, consequent, support, confidence, lift))
        
        return association_rules

.. code:: ipython3

    transactions_file = "outputaudio.txt"
    min_support = 4
    transactions = read_transactions(transactions_file)
    freq_itemsets = get_frequent_itemsets(transactions, min_support)
    a = generate_association_rules(freq_itemsets, transactions, .7)
    print(freq_itemsets)
    print(a)

.. code:: ipython3

    transactions_file = "outputcv.txt"
    min_support = 3
    transactions = read_transactions(transactions_file)
    freq_itemsets = get_frequent_itemsets(transactions, min_support)
    print(freq_itemsets)

.. code:: ipython3

    transactions_file = "outputgeneral.txt"
    min_support = 4
    transactions = read_transactions(transactions_file)
    freq_itemsets = get_frequent_itemsets(transactions, min_support)
    print(freq_itemsets)

.. code:: ipython3

    transactions_file = "outputgraphs.txt"
    min_support = 3
    transactions = read_transactions(transactions_file)
    freq_itemsets = get_frequent_itemsets(transactions, min_support)
    print(freq_itemsets)

.. code:: ipython3

    transactions_file = "outputNLP.txt"
    min_support = 30
    transactions = read_transactions(transactions_file)
    freq_itemsets = get_frequent_itemsets(transactions, min_support)
    a = generate_association_rules(freq_itemsets, transactions, .7)
    print(freq_itemsets)
    print(a)

.. code:: ipython3

    transactions_file = "outputRL.txt"
    min_support = 7
    transactions = read_transactions(transactions_file)
    freq_itemsets = get_frequent_itemsets(transactions, min_support)
    a = generate_association_rules(freq_itemsets, transactions, .7)
    print(freq_itemsets)
    print(a)

.. code:: ipython3

    transactions_file = "outputsqe.txt"
    min_support = 8
    transactions = read_transactions(transactions_file)
    freq_itemsets = get_frequent_itemsets(transactions, min_support)
    a = generate_association_rules(freq_itemsets, transactions, .7)
    print(freq_itemsets)
    print(a)

.. code:: ipython3

    import pandas as pd
    import json
    
    # load the JSON file as a dictionary
    with open('tmpyqn0g7vm.json', 'r') as f:
        data = json.load(f)
    # data = pd.json_normalize(data)
    # convert the dictionary to a dataframe
    
    df1 = pd.DataFrame.from_dict(data)
    df1['modalities'] = df1['modalities'].str[0]
    df1['uses'] = df1['url'].apply(lambda x: boringfunc(x))

.. code:: ipython3

    import csv
    
    # read the text file and split its contents into rows
    with open('a', 'r') as f:
        lines = f.readlines()
    
    # parse the first line to extract column names
    header = lines[0].strip().split(',')
    
    # create and write CSV file
    with open('data.csv', mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header) # write header row
        for line in lines[1:]: # iterate through remaining lines
            row = line.strip().replace('"','').split(',',2)
            writer.writerow(row) # write data row

.. code:: ipython3

    df = pd.read_csv('data.csv')
    a = []
    for i in df.groupby(['project_type','function']).groups:
        a.append(df.groupby(['project_type','function']).get_group(i))

.. code:: ipython3

    import json
    def convert(x):
        x= str(x)
        dictionary = json.loads(x.replace("'", "\""))
    
        result = []
        
        for i,j in dictionary.items():
            if type(j) == str:
                result.append(hash_string(j))
            else:
                result.append(j)
        return result
        

.. code:: ipython3

    a[0]['keywords'] = a[0]['keywords'].apply(lambda x:convert(x))

.. code:: ipython3

    a[0]

.. code:: ipython3

    df1['modalities'] = df1['modalities'].fillna("others")

.. code:: ipython3

    df1['modalities'].unique()

.. code:: ipython3

    df1.to_csv()

.. code:: ipython3

    def boringfunc(x):
        types = []
        soup = BeautifulSoup(requests.get(x).content, 'html.parser')
        selected_option = soup.find_all('option', selected=True)
        for option in selected_option:
            text = option.text.replace('\n','').lower()
            types.append(text)
        return list(set(types))

.. code:: ipython3

    from bs4 import BeautifulSoup
    import requests
    soup = BeautifulSoup(requests.get('https://paperswithcode.com/dataset/mnist').content, 'html.parser')

.. code:: ipython3

    boringfunc('https://paperswithcode.com/dataset/mnist')

.. code:: ipython3

    df1.to_csv('webscrap.csv', index = False)

.. code:: ipython3

    import pandas as pd
    df1 = pd.read_csv('webscrap.csv')

.. code:: ipython3

    df1

.. code:: ipython3

    df1['modalities'].fillna("others")

.. code:: ipython3

    df1 = df1[df1['uses']  != "[]"]

.. code:: ipython3

    a = []
    for i in df1.groupby('modalities').groups:
        a.append(df1.groupby('modalities').get_group(i))

.. code:: ipython3

    df1['modalities'].unique()

.. code:: ipython3

    with open('outputaudio.txt', 'w') as file:
        for index, row in a[0].iterrows():
            row_string = row.values[1].replace('[', '').replace(']', '').replace("'", '')
            file.write(row_string + '\n')
