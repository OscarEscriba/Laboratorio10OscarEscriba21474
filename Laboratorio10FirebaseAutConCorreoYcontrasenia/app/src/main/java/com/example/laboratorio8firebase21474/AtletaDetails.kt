package com.example.laboratorio8firebase21474

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.ktx.Firebase
import org.w3c.dom.Text
import java.sql.RowId

class AtletaDetails : AppCompatActivity() {
    private lateinit var tvAtlId: TextView
    private lateinit var tvAtlName: TextView
    private lateinit var tvAtlAge: TextView
    private lateinit var tvAtlDeporte: TextView
    private lateinit var btnUpdate:Button
    private lateinit var btnDelete:Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_atleta_details)
        initView()
        setValuesToView ()

        btnUpdate.setOnClickListener{
            openUpdateDialog(
                intent.getStringExtra("AtlId").toString(),
                intent.getStringExtra("AtlName").toString(),
            )
        }
        btnDelete.setOnClickListener{
            deleteRecord(
                intent.getStringExtra("Aid").toString()
            )
        }
    }
    private fun deleteRecord(
        id:String
    ) {
        val dbRef = FirebaseDatabase.getInstance().getReference("Employees").child(id)
        val aTask = dbRef.removeValue()

        aTask.addOnSuccessListener {
            Toast.makeText(this, "La informacion del atleta ha sido eliminada", Toast.LENGTH_LONG).show()
            val intent = Intent(this, FetchingActivity::class.java)
            finish()
            startActivity(intent)
        }.addOnFailureListener{
            error ->
            Toast.makeText(this, "Error ${error.message}", Toast.LENGTH_LONG).show()
        }
    }
    private fun initView(){
    }
    private fun setValuesToView () {
        tvAtlId.text = intent.getStringExtra("AtlId")
        tvAtlName.text=intent.getStringExtra("AtlName")
        tvAtlAge.text=intent.getStringExtra("AtlAge")
        tvAtlDeporte.text=intent.getStringExtra("AtlDeporte")
    }
    private fun openUpdateDialog(
        AtlId: String,
        AtlName: String
    ) {
        val aDialog = AlertDialog.Builder(this)
        val inflater = layoutInflater
        val aDialogView = inflater.inflate(R.layout.update_dialog, null)

        aDialog.setView(aDialogView)

        val etAtlName = aDialogView.findViewById<EditText>(R.id.etAtlName)
        val etAtlEdad = aDialogView.findViewById<EditText>(R.id.etAtlAge)
        val etAtlDeporte = aDialogView.findViewById<EditText>(R.id.etAtlDeporte)
        val btnUpdateData = aDialogView.findViewById<Button>(R.id.btnUpdateData)

        etAtlName.setText(intent.getStringExtra("atlName").toString())
        etAtlEdad.setText(intent.getStringExtra("atlAge").toString())
        etAtlDeporte.setText(intent.getStringExtra("atlDeporte").toString())

        aDialog.setTitle("Updating $AtlName record")

        val AlertDialog = aDialog.create()
            AlertDialog.show()

        btnUpdateData.setOnClickListener{
            updateAtlData (
                AtlId,
                etAtlName.text.toString(),
                etAtlEdad.text.toString(),
                etAtlDeporte.text.toString()
                )
            Toast.makeText(applicationContext, "Datos del atleta Actualizados", Toast.LENGTH_LONG).show()

            tvAtlName.text=etAtlName.text.toString()
            tvAtlAge.text=etAtlEdad.text.toString()
            tvAtlDeporte.text=etAtlDeporte.text.toString()

            AlertDialog.dismiss()
        }
    }

    private fun updateAtlData (
        id:String,
        name:String,
        age:String,
        deporte:String
    ) {
        val dbRef = FirebaseDatabase.getInstance().getReference("Employees").child(id)
        val atlInfo = AtletaModel(id, name, age, deporte)
        dbRef.setValue(atlInfo)
    }
}