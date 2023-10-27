package com.example.laboratorio8firebase21474

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.provider.ContactsContract.CommonDataKinds.Email
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AlertDialog
import com.google.firebase.auth.FirebaseAuth

class AuthActivity : AppCompatActivity() {
    private lateinit var btnInsertData: Button
    private lateinit var btnFetching: Button
    private lateinit var btnSignUp : Button
    private lateinit var btnAcceder: Button
    private lateinit var etEmail: EditText
    private lateinit var etPassword: EditText

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_auth)
        //______________________________________________________________________________________________
        //este es para instanciar la base de datos (creo que no la vamos a necesitar en este archivo de codigo...

        //_______________________________________________________________________________________________
        btnInsertData = findViewById(R.id.button)
        btnFetching = findViewById(R.id.button2)
        btnSignUp = findViewById(R.id.button3)
        btnAcceder = findViewById(R.id.button4)
        etEmail = findViewById(R.id.etEmail)
        etPassword = findViewById(R.id.etPassword)

        //________________________________________________________________________________________________
        btnInsertData.setOnClickListener{
            val intent = Intent(this, InsertActivity::class.java)
            startActivity(intent)
        }

        btnFetching.setOnClickListener{
            val intent = Intent(this, FetchingActivity:: class.java)
            startActivity(intent)
        }

        //setup
        setup()
    }
    private fun setup() {
        title ="Autenticacion"
        btnSignUp.setOnClickListener {
            if (etEmail.text.isNotEmpty() && etPassword.text.isNotEmpty()) {
                FirebaseAuth.getInstance().createUserWithEmailAndPassword(etEmail.text.toString(), etPassword.text.toString()).addOnCompleteListener {
                    if(it.isSuccessful) {
                        showHome(it.result?.user?.email ?:"", ProviderType.BASIC)
                    }else {
                        alerts()
                    }
                }
            }
        }
        btnAcceder.setOnClickListener {
            if (etEmail.text.isNotEmpty() && etPassword.text.isNotEmpty()) {
                FirebaseAuth.getInstance()
                    .signInWithEmailAndPassword(etEmail.text.toString(), etPassword.text.toString()).addOnCompleteListener {
                    if(it.isSuccessful) {
                        showHome(it.result?.user?.email ?:"", ProviderType.BASIC)
                    }else {
                        alerts()
                    }
                }
            }
        }


    }
    private fun alerts() {
        val builder =AlertDialog.Builder(this)
        builder.setTitle("error")
        builder.setMessage("Se ha producido un error")
        builder.setPositiveButton("aceptar", null)
        val dialog: AlertDialog =builder.create()
        dialog.show()
    }
    private fun showHome(email: String, provider: ProviderType){
        val intent = Intent(this, InsertActivity::class.java)
        startActivity(intent)
    }
}