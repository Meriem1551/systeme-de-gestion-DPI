import { Component } from '@angular/core';
import { Router } from '@angular/router';
@Component({
  selector: 'app-landing-page',
  imports: [],
  templateUrl: './landing-page.component.html',
  styleUrl: './landing-page.component.css',
  standalone: true,
})
export class LandingPageComponent {
constructor(private router: Router){}

navigateToLogin(): void{
  this.router.navigate(['/login']);
}

}
