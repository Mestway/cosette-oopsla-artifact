package custom;

import java.util.Map;

import java.util.HashMap;

import catg.CATG;
import database.table.SymbolicTable;
import database.table.commands.SelectCommand;
import database.table.from.From;
import database.table.groupby.*;
import database.table.having.HavingTrue;
import database.table.internals.ForeignKey;
import database.table.internals.Row;
import database.table.internals.Table;
import database.table.internals.TableFactory;
import database.table.operations.*;
import database.table.select.Select;
import database.table.where.Where;

import janala.Main;

import java.sql.ResultSet;

public class EquivTest1b {
    public static int l_c1;

    public static Map<String, Integer> resultSetToMap(ResultSet rs) {
        Map<String, Integer> result = new HashMap<String, Integer>();
        try{
            while (rs.next()) {
                int s = rs.getInt("fid");
                int n = rs.getInt("year");
                String hs = s + "#" + n;
                if (! result.containsKey(hs)) {
                    result.put(hs, 0);
                }
                result.put(hs, result.get(hs) + 1);
            }
        } catch (Exception e) {
            return result;
        }
        return result;
    }

    public static boolean tableEqual(ResultSet rs1, ResultSet rs2) {
        Map<String, Integer> hs1 = resultSetToMap(rs1);
        Map<String, Integer> hs2 = resultSetToMap(rs2);
        if (hs1.size() != hs2.size()) {
            return false;
        }
        for (Map.Entry<String, Integer> k : hs1.entrySet()) {
            if (! hs2.containsKey(k.getKey()) || (hs2.get(k.getKey()) != k.getValue())) {
                return false;
            }
        }
        return true;
    }

    public  static void testme(Table[] tables){

        Table t1 = (new SelectCommand(
                new Select() {
                    public String[] selectAs() { return new String[]{"fid", "year"}; }
                    public Operations[] select() {
                        return new Operations[]{ new IdentityOperation(0, "fid"),
                                                 new SumOperation(0, "year")}; 
                    }
                },
                new From(tables),
                new Where() {
                    @Override
                    public boolean where(Row[] rows) {
                        return rows[0].get("fid").equals(rows[0].get("carrier_id"))
                                && ((Integer) rows[0].get("year") > 2010);
                    }
                },
                new SimpleGroupBy(new String[]{"fid"}),
                new HavingTrue(),
                null,
                false
        )).execute();

        Table t2 = (new SelectCommand(
                new Select() {
                    public String[] selectAs() { return new String[]{"fid", "year"}; }
                    public Operations[] select() {
                        return new Operations[]{ new IdentityOperation(0, "fid"),
                                                 new SumOperation(0, "year")}; 
                    }
                },
                new From(tables),
                new Where() {
                    @Override
                    public boolean where(Row[] rows) {
                        return rows[0].get("fid").equals(rows[0].get("carrier_id"))
                                && ((Integer) rows[0].get("year") > 2010);
                    }
                },
                new SimpleGroupBy(new String[]{"fid", "year"}),
                new HavingTrue(),
                null, 
                false
        )).execute();

        printTable(t1);
        printTable(t2);

        if(tableEqual(t1.getResultSet(), t2.getResultSet())){
            System.out.println("branch 1");
        }
        else{
            System.out.println("branch 2");
        }
    }

    public static void initTable(Table table, int n) {
        int[] types = table.getColumnTypes();
        String[] columnNames = table.getColumnNames();

        // Init table
        for (int i = 0; i < n; i++) {
            Object[] row = new Object[types.length];
            System.out.print(table.getName() + " {");
            for (int j = 0; j < row.length; j++) {
                if (types[j] == Table.INT) {
                    int x = Main.readInt(i);
                    Main.MakeSymbolic(x);
                    Integer k = new Integer(x);
                    row[j] = k;
                }
                System.out.print(row[j]);
                System.out.print(" , ");
            }
            System.out.println("}");
            table.insert(row);
        }
    }

    public static void initTable2(Table table, int n) {
        int[] types = table.getColumnTypes();
        String[] columnNames = table.getColumnNames();

        int y = Main.readInt(0);
        Main.MakeSymbolic(y);

        // Init table
        for (int i = 0; i < n; i++) {
            Object[] row = new Object[types.length];
            System.out.print(table.getName() + " {");
            for (int j = 0; j < row.length; j++) {
                if (types[j] == Table.INT) {
                    if (j == 0) {
                        row[j] = y;
                    } else {
                        int x = Main.readInt(i);
                        Main.MakeSymbolic(x);
                        Integer k = new Integer(x);
                        row[j] = k;
                    }
                }
                System.out.print(row[j]);
                System.out.print(" , ");
            }
            System.out.println("}");
            table.insert(row);
        }
    }

    public static void printTable(Table table) {
        String[] columnNames = table.getColumnNames();
        ResultSet rs = table.getResultSet();
        System.out.println("----------");
        try {
            while (rs.next()) {
                System.out.print("{ ");
                for (String s : columnNames) {
                    System.out.print(rs.getInt(s) + ", "); 
                }  
                System.out.println(" }");
            }
        } catch (Exception e) {
            System.out.println("wrong");
        }
    }

    public static void main(String[] args){

        Table smallFlights = TableFactory.create("small_flight", 
            new String[]{"fid", "year", "carrier_id" }, 
            new int[]{Table.INT, Table.INT, Table.INT}, 
            new int[]{Table.NONE, Table.NONE, Table.NONE}, 
            new ForeignKey[]{null, null, null});

        initTable(smallFlights, Integer.parseInt(args[0]));

        testme(new Table[]{smallFlights});
    }
}
