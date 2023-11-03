package com.example.laboratorio8firebase21474

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.renderscript.Sampler.Value
import android.speech.tts.TextToSpeech
import android.view.View
import android.widget.LinearLayout
import android.widget.TextView
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener


class FetchingActivity : AppCompatActivity() {
    private lateinit var AtlRecyclerView: RecyclerView
    private lateinit var tvLoadingData: TextView
    private lateinit var atlList: ArrayList<AtletaModel>
    private lateinit var  dbRef: DatabaseReference
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_fetching)

        AtlRecyclerView = findViewById(R.id.rvEmp)
        AtlRecyclerView.layoutManager = LinearLayoutManager(this)
        AtlRecyclerView.setHasFixedSize(true)
        tvLoadingData = findViewById(R.id.tvLoadingData)

        atlList = arrayListOf<AtletaModel>()
        getAtletasData()
    }

    private fun getAtletasData(){
        AtlRecyclerView.visibility = View.GONE
        tvLoadingData.visibility = View.VISIBLE

        dbRef = FirebaseDatabase.getInstance().getReference("Employees")
        dbRef.addValueEventListener(object : ValueEventListener{
            override fun onDataChange(snapshot: DataSnapshot) {
                atlList.clear()
                if (snapshot.exists()){
                    for (atlSnap in snapshot.children){
                        val atlData = atlSnap.getValue((AtletaModel::class.java))
                        atlList.add(atlData!!)
                    }
                    val mAdapter = AtletaAdapter(atlList)
                    AtlRecyclerView.adapter = mAdapter

                    mAdapter.setOnItemClickListener(object: AtletaAdapter.onItemClickListener {
                        override fun onItemClick(position: Int) {
                            val intent = Intent(this@FetchingActivity, AtletaDetails:: class.java)

                            //put extras
                            intent.putExtra("atlID", atlList[position].Aid)
                            intent.putExtra("atlName", atlList[position].Anombre)
                            intent.putExtra("atlAge", atlList[position].Aedad)
                            intent.putExtra("atlDeporte", atlList[position].Adeporte)
                            startActivity(intent)
                        }

                    })

                    AtlRecyclerView.visibility = View.VISIBLE
                    tvLoadingData.visibility = View.GONE
                }
            }

            override fun onCancelled(error: DatabaseError) {
                TODO("Not yet implemented")
            }

        })
     }
}