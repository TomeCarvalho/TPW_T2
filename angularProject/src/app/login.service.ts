import {Injectable} from '@angular/core';
import {environment} from "../environments/environment";
import {HttpClient, HttpHeaders} from "@angular/common/http";

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
}

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  token: string

  constructor(private http: HttpClient) {
    this.token = ""
  }

  login(username: string, password: string) {
    console.log(`LoginService.login: Sending ${{"username": username, "password": password}}`)
    this.http.post<any>(
      `${environment.apiUrl}/token-auth`,
      {"username": username, "password": password},
      httpOptions
    ).subscribe(data => {
      if (data.status == 200) {
        console.log(`LoginService.login: Authentication request successful (token: ${data.token}).`)
        this.token = data.token
      } else { // 400 Bad Request
        console.log(`LoginService.login: Authentication request unsuccessful: ${data.non_field_errors}`)
      }
      return data
    })
  }

  logout() {
    this.token = ""
  }
}
