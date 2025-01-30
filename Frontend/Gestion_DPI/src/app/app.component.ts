import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';




@Component({
  selector: 'app-root',

  imports: [CommonModule, RouterOutlet],


  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  title = "Système de Gestion DPI - Amejay"
}
