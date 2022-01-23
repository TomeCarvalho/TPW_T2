import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {LoginService} from "./login.service";

@Injectable({
  providedIn: 'root'
})
export class HistoryService {

  private baseURL = 'http://localhost:8000/ws/history/'

  constructor(private http: HttpClient, private loginService: LoginService) { }

  getInfo(infoUrl: string){
    const url = this.baseURL + infoUrl
    let header = {};
    if (this.loginService.token()){
      header = {

        headers: new HttpHeaders()
          .set('Authorization',  `Token ${(this.loginService.token())}`)
      }
    }
    return this.http.get<any>(url, header);
  }
}
