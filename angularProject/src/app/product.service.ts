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

  getDashboard(): Observable<Product[]>{
    const url = this.baseURL + 'dashboard';
    let header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Token ${(this.loginService.token())}`)
    }
    return this.http.get<Product[]>(url, header);
  }

  getMyProducts(): Observable<Product[]>{
    const url = this.baseURL + 'my-products';
    let header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Token ${(this.loginService.token())}`)
    }

    return this.http.get<Product[]>(url, header);
  }
}

