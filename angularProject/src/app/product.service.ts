import { Injectable } from '@angular/core';
import { Product} from "./product";
import { Observable } from "rxjs/internal/Observable";
import {HttpClient, HttpHeaders} from "@angular/common/http";

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  private baseURL = 'http://localhost:8000/ws/'

  constructor(private http: HttpClient) { }

  getProducts(): Observable<Product[]>{
    const url = this.baseURL + 'products';
    return this.http.get<Product[]>(url);
  }
}

