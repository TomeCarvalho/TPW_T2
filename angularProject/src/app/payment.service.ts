import { Injectable } from '@angular/core';
import {HttpClient, HttpErrorResponse, HttpHeaders} from "@angular/common/http";
import {environment} from "../environments/environment";
import {catchError, throwError} from "rxjs";
import {LoginService} from "./login.service";


@Injectable({
  providedIn: 'root'
})
export class PaymentService {

  private baseURL = 'http://localhost:8000/ws/'

  constructor(private loginService: LoginService, private http: HttpClient) { }

  checkout(data: any): Promise<boolean>{
    console.log("CHECKOUT")
    let promise = new Promise<boolean>((resolve, reject) => {
      let header = {
        headers: new HttpHeaders()
          .set('Authorization',  `Token ${(this.loginService.token())}`)
      }
      this.http.post<any>(
        `${environment.apiUrl}/cart/checkout`,
        data,
        header
      )
        .pipe(catchError((err) => {
          console.log(err)
          reject(false)
          return PaymentService.handleError(err)
        }))
        .subscribe(data => {
          console.log(`ProductService.add_to_cart: Adding to cart successful.`)
          console.log(data)
          if(data == 200){
            resolve(true)
          }
          else {
            console.log("BAD FALSE")
            reject(false)
          }

          return data
        })
    })
    return promise
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
