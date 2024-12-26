import { Component } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {
  headerText: string = 'Agal Imene';
  logoUrl: string = 'assets/images/Logo.svg';
}
