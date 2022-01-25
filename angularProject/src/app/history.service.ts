import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {LoginService} from "./login.service";
import {environment} from "../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class HistoryService {

  private baseURL = `${environment.apiUrl}`

  constructor(private http: HttpClient, private loginService: LoginService) { }

  getInfo(infoUrl: string){
    const url = this.baseURL + 'history/' + infoUrl
    console.log(url)
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
