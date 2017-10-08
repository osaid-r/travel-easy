package com.hacks.android.dequeue;

import android.os.Handler;
import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
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
import java.util.Random;
import java.util.concurrent.TimeUnit;

public class MainActivity extends AppCompatActivity {

    public static final String url = "jdbc:mysql://139.59.69.74/tumchai";
    public static final String user = "temp";
    public static final String password = "pass";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ((Button) findViewById(R.id.button)).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast.makeText(MainActivity.this, ((EditText) findViewById(R.id.editText)).getText().toString(), Toast.LENGTH_SHORT).show();
            }
        });
        display();
    }

    private void display(){


        String result = "";
        try{
//            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
//            StrictMode.setThreadPolicy(policy);

            //Class.forName("com.mysql.jdbc.Driver");
//            Connection connection = DriverManager.getConnection(url,user,password);
//            Statement statement = connection.createStatement();
//            ResultSet resultSet = statement.executeQuery("Select * from TODO");

            double sum = 0;
            float avg=0;
            int counter = 1;
            while (counter<=20){
//                runOnUiThread(new Runnable() {
//                    @Override
//                    public void run() {
//                        final Handler handler = new Handler();
//                        handler.postDelayed(new Runnable() {
//                            @Override
//                            public void run() {
//                                                 //add your code here
//                            }
//                        }, 1000);
//                    }
//                });


                Log.d("HACCKKKKKKKK ==========", "display: ");
                double number = Math.random()*20 +3;
                ((TextView) findViewById(R.id.tv_ln1CurrSpeed)).setText(Float.toString((float)number));
                sum += number;
                avg = (float)sum/counter;
                counter++;

                ((TextView) findViewById(R.id.tv_ln1AvgSpeed)).setText(Float.toString((float)(number-2.1324)));




                //TimeUnit.SECONDS.sleep(3);



            }
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
