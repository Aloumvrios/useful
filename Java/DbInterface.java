import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;
import org.slf4j.ext.XLogger;
import org.slf4j.ext.XLoggerFactory;

public class DBInterface {

    private final XLogger logger = XLoggerFactory.getXLogger(this.getClass());
    private Connection connection;
    private final ConManager manager;

    public DBInterface() {
        this.manager = new ConManager();
    }

    // ********************************************************************************************************************************
    // Symptoms_Data Table methods
    // ********************************************************************************************************************************
    public void storeSymptomDatatoDB(ArrayList<SymptomData> Data) {
        logger.entry(Data.size());
        String sql = "INSERT INTO SYMPTOM_DATA (COLUMN1,COLUMN2,COLUMN3,COLUMN4,COLUMN5,COLUMN6) VALUES(?,?,?,?,?,?)";
        try {
            connection = manager.getConnectionFromPool("TABLE_NAME");
            PreparedStatement preparedStatement = connection.prepareStatement(sql);

            for (int i = 0; i < Data.size(); i++) {
                preparedStatement.setString(1, Data.get(i).getAttribute1());
                preparedStatement.setString(2, Data.get(i).getAttribute2());
                preparedStatement.setString(3, Data.get(i).getAttribute3());
                preparedStatement.setTimestamp(4, Data.get(i).getAttribute4()); //for timestamp format
                preparedStatement.setString(5, Data.get(i).getAttribute5());
                preparedStatement.setString(6, Data.get(i).getAttribute6());
                preparedStatement.addBatch();
            }
            int[] updateCount = preparedStatement.executeBatch();
            checkUpdateCounts(updateCount);
        } catch (SQLException e) {
            logger.catching(e);
        } finally {
            closeConnection(connection);
        }
        logger.exit();
    }

    public ArrayList<SymptomData> retrieveSymptomDataFromDB(String attribute3, String attribute2) {
        logger.entry();
        ArrayList<SymptomData> resultList = new ArrayList<>();
        String sql = "SELECT * FROM SYMPTOM_DATA WHERE COLUMN3= ? AND COLUMN2= ?";
        try {
            connection = manager.getConnectionFromPool("TABLE_NAME");
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, neName);
            preparedStatement.setString(2, caseID);
            try (ResultSet rs = preparedStatement.executeQuery()) {
                while (rs.next()) {
                    SymptomData Data = new SymptomData();
                    Data.getAttribute7(rs.getString("COLUMN7"));
                    Data.getAttribute1(rs.getString("COLUMN1"));
                    Data.getAttribute2(rs.getString("COLUMN2"));
                    Data.getAttribute3(rs.getString("COLUMN3"));
                    Data.getAttribute4(rs.getTimestamp("COLUMN4"));
                    Data.getAttribute5(rs.getString("COLUMN5"));
                    Data.getAttribute6(rs.getString("COLUMN6"));
                    resultList.add(Data);
                }
            }
        } catch (SQLException e) {
            logger.catching(e);
        } finally {
            closeConnection(connection);
        }
        logger.exit();
        return resultList;
    }

    public int countOccurenciesSince(String attribute2, String attribute3, String range, String attribute5) {
        logger.entry();
        logger.debug("attribute 2 "+attribute2+" attribute 3 "+attribute3+" attribute 5 "+attribute5+" range "+range);
        int count = 0;
        String sql = "select count(*) "
                + "from SYMPTOM_DATA "
                + "where COLUMN2=? and "
                + "COLUMN3=? and "
                + "COLUMN5=? and "
                + "COLUMN4 >= to_timestamp(add_months(sysdate,-?))";
        try {
            connection = manager.getConnectionFromPool("TABLE_NAME");
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, attribute2);
            preparedStatement.setString(2, attribute3);
            preparedStatement.setString(3, attribute5);
            preparedStatement.setString(4, range);
            try (ResultSet rs = preparedStatement.executeQuery()) {
                if (rs.next()) {
                    count = rs.getInt("count(*)");
                }
            }
        } catch (SQLException e) {
            logger.catching(e);
        } finally {
            closeConnection(connection);
        }
        logger.exit(count);
        return count;
    }

    private void closeConnection(Connection connection) {
        try {
            connection.close();
        } catch (SQLException e) {
            logger.error("Unable to close connection!", e);
        } finally {
            connection = null;
        }
    }
