import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class RechercheService {

  private apiUrl = 'http://127.0.0.1:8000/api/dpi/dpis/';
  private searchApiUrl = 'http://127.0.0.1:8000/api/dpi/NssSearch/';
  private scanApiUrl = 'http://127.0.0.1:8000/api/dpi/QRCodeSearch/';  // Base URL for QR code search

  constructor(private http: HttpClient) {}

  getDpiList(): Observable<any> {
    return this.http.get(this.apiUrl);
  }
  searchDpiByNss(nss: string): Observable<any> {
    const params = new HttpParams().set('nss', nss); // Adding NSS as query parameter
    return this.http.get(this.searchApiUrl, { params });
  }

  scanQRCode(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post(this.scanApiUrl, formData);
  }

}

