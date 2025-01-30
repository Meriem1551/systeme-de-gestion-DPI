import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class CreationDPIService {
  private apiUrl = 'http://127.0.0.1:8000/api/dpi/create-dpi/'; // URL de l'API

  constructor(private http: HttpClient) { }

  createDPI(dpiData:any): Observable<any> {
    return this.http.post(this.apiUrl, dpiData);
  }

}

