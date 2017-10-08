package com.hacks.android.dequeue;

import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.Statement;

public class MainActivity extends AppCompatActivity {

    public static final String url = "";
    public static final String user = "";
    public static final String password = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        display();
    }

    private void display(){

        String result = "";
        try{
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);

            Class.forName("com.mysql.jdbc.Driver");
            Connection connection = DriverManager.getConnection(url,user,password);
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery("Select * from TODO");
            ResultSetMetaData resultSetMetaData = resultSet.getMetaData();

            double sum = 0;
            double avg;
            int counter = 1;
            while (resultSet.next()){
                ((TextView) findViewById(R.id.tv_ln1CurrSpeed)).setText(resultSet.getString(2));
                sum += Integer.parseInt(resultSet.getString(2));
                avg = sum/counter;
                counter++;
                ((TextView) findViewById(R.id.tv_ln1AvgSpeed)).setText(Double.toString(avg));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
