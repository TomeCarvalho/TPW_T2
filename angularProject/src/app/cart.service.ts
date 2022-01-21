import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {LoginService} from "./login.service";
import {Observable} from "rxjs";
import {ProductInstance} from "./product_instance";

@Injectable({
  providedIn: 'root'
})
export class CartService {

  private baseURL = 'http://localhost:8000/ws/'

  constructor(private http: HttpClient, private loginService: LoginService) { }

  getCart(): Observable<ProductInstance[]>{
    const url = this.baseURL + "cart";
    let header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Token ${(this.loginService.token())}`)
    }
    return this.http.get<ProductInstance[]>(url, header);
  }

  deleteInstance(prod_inst: ProductInstance){
    const url = this.baseURL + "cart";
    let header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Token ${(this.loginService.token())}`),
      body: {productInstance: prod_inst}
    }
    console.log("PAPAPAPAPAP")
    return this.http.delete<any>(url, header)
  }
}
