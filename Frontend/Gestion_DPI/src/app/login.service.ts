import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  private apiUrl = 'http://127.0.0.1:8000/api/v1/auth/login/';

  constructor(private http: HttpClient, private router: Router) {}

login(email: string, password:string):Observable<any>{
    return this.http.post(this.apiUrl, {email,password});

}

handleLoginSuccess(response: any): void {

     const { role, id, full_name, access_token, refresh_token } = response;

  // Store tokens in localStorage
  localStorage.setItem('fullname', full_name);
  localStorage.setItem('id', id.toString());
  localStorage.setItem('access_token', access_token);
  localStorage.setItem('refresh_token', refresh_token);
  localStorage.setItem('role', role);

    console.log('Navigating based on role:', role);

    // Navigate based on the user's role
    if (role === 'admin') {
      this.router.navigateByUrl('/creation-dpi');
    }if (role === 'patient') {
      this.router.navigate(['/consulter-dpi', id,role], { queryParams: { role: role } });
    }else if (role === 'medecin') {
      this.router.navigate(['/recherche-patient']);
    } else if (role === 'infirmier') {
      // Pass the infirmier_id as a query parameter
      this.router.navigate(['/soins-infirmiers'], { queryParams: { id } });
    } else if (role === 'pharmacien'){
      this.router.navigate(['']);
    }else if (role === 'laborantin'){
      this.router.navigate(['/page-laborantin']);
    } else if (role === 'radiologue'){
      this.router.navigate(['/page-radiologue']);
    }
  }
}