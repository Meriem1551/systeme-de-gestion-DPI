import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms'; 
import { LoginService } from '../login.service';
@Component({
  selector: 'app-login',
  imports: [FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
  standalone:true
})
export class LoginComponent {
title = 'Connexion';
text='Bienvenue à Amejay, votre portail vers une gestion médicale simplifiée et efficace !';
label1 = `Email`;
label2 = 'Mot de passe';
ph1=`Votre email`;
ph2='Votre mot de passe';
button='Se Connecter';
name1='email';
name2='password';

email = '';
password = '';

constructor(private loginService: LoginService) { }

onSubmit(): void{
  this.loginService.login(this.email, this.password).subscribe({
    next: (response) => {
      console.log('Login successful:', response);
      this.loginService.handleLoginSuccess(response);
    },
    error: (err) => {
      console.error('Login failed:', err);
      alert('Login failed. Please check your email and password.');
    },
  });

}

}
