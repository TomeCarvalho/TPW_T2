import { Injectable } from '@angular/core';
import { Product} from "./product";
import { Observable } from "rxjs/internal/Observable";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {LoginService} from "./login.service";

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  private baseURL = 'http://localhost:8000/ws/'

  constructor(private http: HttpClient, private loginService: LoginService) { }

  getProducts(source: string, query: string): Observable<Product[]>{
    const url = this.baseURL + source + query;
    let header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Token ${(this.loginService.token())}`)
    }
    return this.http.get<Product[]>(url, header);
  }

  getGroups(){
    const url = this.baseURL + "groups"
    let header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Token ${(this.loginService.token())}`)
    }
    return this.http.get<any>(url, header);
  }

}

