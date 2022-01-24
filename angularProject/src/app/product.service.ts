import { Injectable } from '@angular/core';
import {environment} from "../environments/environment";
import { Product} from "./product";
import { Observable } from "rxjs/internal/Observable";
import {HttpClient, HttpErrorResponse, HttpHeaders} from "@angular/common/http";
import {LoginService} from "./login.service";
import {catchError, throwError} from "rxjs";

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
    let header = {};
    if (this.loginService.token()){
      header = {

        headers: new HttpHeaders()
          .set('Authorization',  `Token ${(this.loginService.token())}`)
      }
    }
    return this.http.get<Product[]>(url, header);
  }

  getProduct(id: number): Observable<Product> {
    const url = this.baseURL + "products/" + id;
    let header = {};
    if (this.loginService.token()){
      header = {

        headers: new HttpHeaders()
          .set('Authorization',  `Token ${(this.loginService.token())}`)
      }
    }
    return this.http.get<Product>(url, header);
  }

  addProduct(product: Product): Promise<boolean>{
    console.log("CHECKOUT")
    let promise = new Promise<boolean>((resolve, reject) => {
      console.log("Add Product")
      let header = {};
      if (this.loginService.token()) {
        header = {
          headers: new HttpHeaders()
            .set('Authorization', `Token ${(this.loginService.token())}`)
        }
      }
      this.http.post<any>(
        `${environment.apiUrl}/my-products`,
        product,
        header
      )
        .pipe(catchError(ProductService.handleError))
        .subscribe(data => {
          console.log(`LoginService.signup: Authentication request successful.`)
          console.log(data)
          if (data == 400) {
            console.log("BAD FALSE")
            reject(false)
          } else {
            resolve(true)
          }
          //this.appComponent.LogIn()
          return data
        })
    })
    return promise;
  }

  getGroups(){
    const url = this.baseURL + "groups"
    let header = {};
    if (this.loginService.token()){
      header = {

        headers: new HttpHeaders()
          .set('Authorization',  `Token ${(this.loginService.token())}`)
      }
    }
    return this.http.get<any>(url, header);
  }

  add_to_cart(product_id: number, quantity: number) {

    let header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Token ${(this.loginService.token())}`)
    }
    this.http.post<any>(
      `${environment.apiUrl}/cart`,
      {"product_id": product_id, "quantity": quantity},
      header
    )
      .pipe(catchError(ProductService.handleError))
      .subscribe(data => {
        console.log(`ProductService.add_to_cart: Adding to cart successful.`)
        return data
      })
  }

  addStock(product_id: number, quantity: number) {
    let header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Token ${(this.loginService.token())}`)
    }
    this.http.post<any>(
      `${environment.apiUrl}/add-product-stock`,
      {"product_id": product_id, "quantity": quantity},
      header
    )
      .pipe(catchError(ProductService.handleError))
      .subscribe(data => {
        console.log(`ProductService.addStock: Adding stock successful.`)
        return data
      })
  }

  addImage(product_id: number, image: string) {
    let header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Token ${(this.loginService.token())}`)
    }
    this.http.post<any>(
      `${environment.apiUrl}/add-product-img`,
      {"product_id": product_id, "image": image},
      header
    )
      .pipe(catchError(ProductService.handleError))
      .subscribe(data => {
        console.log(`ProductService.addImage: Adding image successful.`)
        return data
      })
  }

  addGroup(product_id: number, group: string) {
    let header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Token ${(this.loginService.token())}`)
    }
    this.http.post<any>(
      `${environment.apiUrl}/add-product-group`,
      {"product_id": product_id, "group": group},
      header
    )
      .pipe(catchError(ProductService.handleError))
      .subscribe(data => {
        console.log(`ProductService.addGroup: Adding group successful.`)
        return data
      })
  }

  toggleVisibility(product_id: number) {
    let header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Token ${(this.loginService.token())}`)
    }
    this.http.post<any>(
      `${environment.apiUrl}/toggle-product-visibility`,
      {"product_id": product_id},
      header
    )
      .pipe(catchError(ProductService.handleError))
      .subscribe(data => {
        console.log(`ProductService.toggleVisibility: Visibility toggled.`)
        return data
      })
  }

  private static handleError(error: HttpErrorResponse) {
    if (error.status === 0)
      // A client-side or network error occurred. Handle it accordingly.
      console.error(`An error occurred: ${error.error}.`)
    else
      // The backend returned an unsuccessful response code. The response body may contain clues as to what went wrong.
      console.error(`Backend returned code ${error.status}, body was: ${error.error}.`)

    // Return an observable with a user-facing error message.
    return throwError(() => 'Whoops, something went wrong...')
  }
}

