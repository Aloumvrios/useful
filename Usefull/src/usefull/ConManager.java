/*
* NEEDS FIXING
 */

import java.sql.Connection;

import oracle.ucp.jdbc.PoolDataSource;
import oracle.ucp.jdbc.PoolDataSourceFactory;

public class ConManager {

    PoolDataSource poolTableName;

    public ConManager() {
        poolTableName = initConPool(hostname, dbname, username, password);
    }

    private PoolDataSource initConPool(String hostname, String dbname, String username, String password) {

        PoolDataSource poolDataSource = poolDataSourceFactory.getPoolDataSource();
        poolDataSource.setConnectionPoolName(username);
        poolDataSource.setUser(username);
        poolDataSource.setPassword(password);
    }

    public Connection getConnectionFromPool(String user) {
        Connection connection = null;
        PoolDataSource pool;

        pool = user

        connection = pool.getConnection();
        connection.setAutoCommit(true);

        return connection;
    }
