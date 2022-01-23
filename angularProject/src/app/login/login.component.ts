import {Component, OnInit} from '@angular/core';
import {LoginService} from "../login.service";
import {FormBuilder} from "@angular/forms";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm = this.formBuilder.group({
    username: '',
    password: '',
  })

  constructor(private loginService: LoginService, private formBuilder: FormBuilder) {
  }

  onSubmit(data: any): void {
    this.loginService.login(data.username, data.password)
    this.loginForm.reset()
  }

  onSignUp(data: any): void {
    this.loginService.signup(data.username, data.password)
  }

  ngOnInit(): void {
  }
}
