import {Injectable} from '@angular/core';
import {environment} from "../environments/environment";
import {HttpClient, HttpErrorResponse, HttpHeaders} from "@angular/common/http";
import {catchError, throwError} from "rxjs";
import {AppComponent} from "./app.component";
import {Router} from "@angular/router";

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
}

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  private static _token: string
  private static _username: string

  constructor(private http: HttpClient, private router: Router) {
    LoginService._token = ""
    LoginService._username = ""
  }

  login(username: string, password: string) {
    console.log(`LoginService.login: Sending ${{"username": username, "password": password}}`)
    console.log(username)
    console.log(password)
    this.http.post<any>(
      `${environment.apiUrl}/token-auth`,
      {"username": username, "password": password},
      httpOptions
    )
      .pipe(catchError(LoginService.handleError))
      .subscribe(data => {
        LoginService._token = data.token
        LoginService._username = username
        localStorage.setItem('loginToken', LoginService._token)
        localStorage.setItem('username', LoginService._username)
        console.log(`LoginService.login: Authentication request successful.\nToken: ${LoginService._token}`)
        this.router.navigate(['/dashboard'])
        return data
      })
  }

  signup(username: string, password: string) {
    console.log(`LoginService.login: Sending ${{"username": username, "password": password}}`)
    console.log(username)
    console.log(password)
    this.http.post<any>(
      `${environment.apiUrl}/signup`,
      {"username": username, "password": password},
      httpOptions
    )
      .pipe(catchError(LoginService.handleError))
      .subscribe(data => {
        console.log(`LoginService.signup: Authentication request successful.`)
        console.log(data)
        //this.appComponent.LogIn()
        return data
      })
    this.login(username, password)
  }

  logout() {
    LoginService._token = ""
    LoginService._username = ""
    localStorage.setItem("loginToken", "")
    localStorage.setItem("username", "")
    this.router.navigate(['/dashboard'])
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

  public username(): string {
    return String(localStorage.getItem("username"))
  }

  public token(): string {
    return String(localStorage.getItem("loginToken"))
  }
}
