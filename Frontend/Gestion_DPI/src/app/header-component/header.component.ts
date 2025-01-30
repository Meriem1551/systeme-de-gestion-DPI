import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  headerText: string = ''; // This will display the user's full name
  logoUrl: string = 'assets/Logo.png';

  constructor(private router: Router) { }

  ngOnInit(): void {
    // Fetch the full name directly from localStorage
    const fullName = localStorage.getItem('fullname');
    this.headerText = fullName ? fullName : 'Utilisateur'; // Default text if full name is not available
  }

  backToLandingPage() : void {
    this.router.navigate(['/login']);
  }
}
