import clickhouse_connect

class pre_clustering:
    def __init__(self, database:str, username:str, password:str) -> None:
        self.database = database
        self.username = username
        self.password = password
        self.client
        pass
        
    def create_table(self, host:str) -> int:        
        #
        query = "CREATE TABLE IF NOT EXISTS clusters(cell UInt64, clusterId Int16) ENGINE = MergeTree ORDER BY (clusterId);"

        try:
            self.client = clickhouse_connect.get_client(host=host, database=self.database, username=self.username, password=self.password)
            result = self.client.command(query)
            return result
        except ValueError as err:
            print(err)
            return -1

    def get_mcc(self, host:str):
        query = "SELECT mcc FROM towers"
        try:
            self.client = clickhouse_connect.get_client(host=host, database=self.database, username=self.username, password=self.password)
            result = self.client.command(query)
            return result
        except ValueError as err:
            print(err)
            return -1

    
    def get_net(self, host:str):
        query = "SELECT net FROM towers"
        try:
            self.client = clickhouse_connect.get_client(host=host, database=self.database, username=self.username, password=self.password)
            result = self.client.command(query)
            return result
        except ValueError as err:
            print(err)
            return -1
    
    def get_area(self, host:str):
        query = "SELECT area FROM towers"
        try:
            self.client = clickhouse_connect.get_client(host=host, database=self.database, username=self.username, password=self.password)
            result = self.client.command(query)
            return result
        except ValueError as err:
            print(err)
            return -1

    
    def create_cluster(self, host:str, database:str, username:str, password:str) -> int:
        result = self.create_table(host=host, database=database, username=username, password=password)
        
        return 0
    
    
    def get_sub_dataframe(self, dataframe, column, value):
        # This function returns a sub dataframe based on some criteria
        return dataframe[dataframe[column]==value]

    def create(self, dataframe, mcc, net, area, cId):
        df_mcc = self.get_sub_dataframe(dataframe, 'mcc', mcc)
        df_net = self.get_sub_dataframe(df_mcc, 'net', net)
        cluster= self.get_sub_dataframe(df_net, 'area', area)
        nb_rows, nb_cols= cluster.shape
        # Add new column for the cluster Id
        clusterId= cId*np.ones(nb_rows)
        cluster.insert(nb_cols, 'clusterId', clusterId, allow_duplicates=True)

        return cluster


    def run(self, dataframe):
        #
        list_mcc= self.get_elements(dataframe, 'mcc')
        list_net= self.get_elements(dataframe, 'net')
        list_area= self.get_elements(dataframe, 'area')

        Id=1 # Intialise Id of the clusters
        clusters_set= pd.DataFrame(columns=['cell','mcc','net','area','lon','lat','clusterId'])
        for mcc in list_mcc:
            for net in list_net:
                for area in list_area:
                    cluster= self.create(dataframe, mcc, net, area, Id)
                    clusters_set= clusters_set.append(cluster)
                    Id= Id+1

        return clusters_set