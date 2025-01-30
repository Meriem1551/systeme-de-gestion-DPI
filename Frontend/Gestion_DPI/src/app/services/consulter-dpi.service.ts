import { Injectable } from '@angular/core';
import exp from 'constants';
import { Observable,of } from 'rxjs';
import {  HttpClient, HttpParams } from '@angular/common/http';
import { map } from 'rxjs/operators';

export interface ListConsultation {
  date: string;
  NConsultation: number;
  Ordo:string;
  Bilan_bio:string;
  Bilan_rad:string;
  Resume: string;
}

export interface ListMeds {
  medicament : string ;
  dose : string ;
  duree : string ;
  
  }

  export interface ListSoins {
    Date:String;
    Description:string;
    Observation:string;
  }
  export interface SoinsData{
    description:string;
    date_soin: string;
    observation: string ;
  }
  export interface ConsultationData {
    id_consult: number;
    date_consult: string;
    ordonnance: boolean;
    bilan_biologique: boolean;
    bilan_radiologique: boolean;
    resume: boolean;
  }
  
  export interface DpiDetails {
    nss: string;
    nom_patient: string;
    prenom_patient: string;
    date_de_naissance: string; // You can use `Date` type if you need a Date object instead of string
    adresse: string;
    telephone: string;
    mutuelle: string;
    personne_a_contacter: string;
    nom_complet_medecin: string;
    id_dpi: string  ;
  }
@Injectable({
  providedIn: 'root'
})
export class ConsulterDpiService {
  
  private apiUrl = 'http://127.0.0.1:8000/api/miseajourdpi/getConsultations/';
  private soinsurl = 'http://127.0.0.1:8000/api/miseajourdpi/getSoins/';
  private resumesurl = 'http://127.0.0.1:8000/api/miseajourdpi/getResume/';
  private ordourl = 'http://127.0.0.1:8000/api/miseajourdpi/getOrdonnance/';
  private bilanbiourl = 'http://127.0.0.1:8000/api/biology';
  private bilanradurl = 'http://127.0.0.1:8000/api/radiology';
  private infourl = 'http://127.0.0.1:8000/api/dpi/consulterdpi'

  constructor(private http: HttpClient) { }
/*
  getListConsultation(dpi: number):Observable<any>{
    const params = new HttpParams().set('dpi', dpi.toString());
    return  this.http.get<any>(this.apiUrl, { params });
  }*/
    getDpiDetails(id: string): Observable<DpiDetails> {
      return this.http.get<DpiDetails>(`${this.infourl}/${id}/`);
    }
    getListConsultation(dpi: number): Observable<ListConsultation[]> {
      const params = new HttpParams().set('dpi', dpi);
      console.log("hi");
      return this.http.get<ConsultationData[]>(this.apiUrl, { params }).pipe(
        map((data: ConsultationData[]) => 
          data.map(consultation => ({
            NConsultation: consultation.id_consult,        // num_consult -> NConsultation
            date: consultation.date_consult,                // date_consult -> date
            Ordo: consultation.ordonnance ? 'oui' : 'non',  // ordonnance -> Ordo (oui/non)
            Bilan_bio: consultation.bilan_biologique ? 'oui' : 'non',                             // Utiliser vos propres données pour Bilan_bio
            Bilan_rad: consultation.bilan_radiologique ? 'oui' : 'non',                              // Utiliser vos propres données pour Bilan_rad
            Resume: consultation.resume ? 'oui' : 'non'    // resume -> Resume (oui/non)
          }))
        )
      ); 
    }

    getResume(id_consult: number): Observable<any> {
      const params = new HttpParams().set('id_consult', id_consult);
      return this.http.get<any>(this.resumesurl, { params });
    } 
    
    
  getListMeds(id_consult: number):Observable<ListMeds[]>{
    const params = new HttpParams().set('id_consult', id_consult);
      return this.http.get<ListMeds[]>(this.ordourl, { params }).pipe(
        map((data: ListMeds[]) => 
          data.map(med => ({
            medicament: med.medicament,       
            dose: med.dose,               
            duree: med.duree ,  
          }))
        )
      );
  }
  getBilanBiologiquesByIdConsult(id_consult: number): Observable<any> {
    return this.http.get(`${this.bilanbiourl}/dpi/${id_consult}/biobilansparconsult/`);
  }

  getBilanRadiologiquesByIdConsult(id_consult: number): Observable<any> {
    return this.http.get(`${this.bilanradurl}/dpi/${id_consult}/bilanparconsult/`);
  }
  getListSoins(dpi: number):Observable<ListSoins[]>{
      const params = new HttpParams().set('dpi', dpi);
      return this.http.get<SoinsData[]>(this.soinsurl, { params }).pipe(
        map((data: SoinsData[]) => 
          data.map(soin => ({
            Description: soin.description,       
            Date: soin.date_soin,               
            Observation: soin.observation ,  
          }))
        )
      );
  }
 
}
