import {Injectable}  from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class LaborantinService {
  private apiUrl = 'http://127.0.0.1:8000/api/biology/dpis/';
  private bilanUrl = 'http://127.0.0.1:8000/api/biology/dpi/{id_dpi}/bilans-biologiques/';
  private resultasUrl = 'http://127.0.0.1:8000/api/biology/create-bio-measures/';
  private grapheUrl = 'http://127.0.0.1:8000/api/biology/generergraphic/{id_dpi}/1';
  constructor(private http: HttpClient) {}

  getPatientList(): Observable<any> {
    return this.http.get(this.apiUrl);
  }

  getBilanList(id_dpi: number): Observable<any> {
    return this.http.get(this.createBilanUrl(id_dpi));
  }
  createBilanUrl(id_dpi: number): string {
    return this.bilanUrl.replace('{id_dpi}', id_dpi.toString()); // Replace the placeholder with the actual id_dpi
  }

  postBilanResultat(updatedData: any): Observable<any> {
    return this.http.post(this.resultasUrl, updatedData); // Pass the data and headers
  }
  getGraphData(id_dpi: number): Observable<any> {
    const dynamicUrl = this.grapheUrl.replace('{id_dpi}', id_dpi.toString());
    return this.http.get(dynamicUrl); // Use the dynamic URL for fetching data
  }
  


}