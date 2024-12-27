import { Component } from '@angular/core';

@Component({
  selector: 'app-login',
  imports: [],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
  standalone: true,
})
export class LoginComponent {
title = 'Connexion';
text='Bienvenue à Amejay, votre portail vers une gestion médicale simplifiée et efficace !';
label1 = `Nom d’Utilisateur`;
label2 = 'Votre mot de passe';
ph1=`Votre nom d'utilisateur`;
ph2='Votre mot de passe';
button='Se Connecter';
name1='username';
name2='password';
}
