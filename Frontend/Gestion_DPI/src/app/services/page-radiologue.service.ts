import { Injectable } from '@angular/core';
import { Observable,of } from 'rxjs';
import {  HttpClient, HttpParams , HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class PageRadiologueService {
   patienturl = 'http://127.0.0.1:8000/api/radiology/dpis/';
   billansradurl = 'http://127.0.0.1:8000/api/radiology';
   updatebilanradurl = 'http://127.0.0.1:8000/api/radiology/bilan_radiologique'

  constructor(private http: HttpClient) { }

  //(): Observable<any> {}
  getListPatients(): Observable<any> {  
    return this.http.get<any>(this.patienturl);
  } 

  getListBillans(dpi : number): Observable<any> {  
    return this.http.get<any>(`${this.billansradurl}/dpi/${dpi}/radiological-bilans/`);
  } 
  updatebilanrad(bilan_id : number, data: FormData):Observable<any> { 
    const url = `${this.updatebilanradurl}/${bilan_id}/update/` ;
    const headers = new HttpHeaders();
    headers.append('Accept', 'application/json');
    return this.http.put(url, data, { headers });

  }


}
