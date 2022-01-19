import { Component, OnInit } from '@angular/core';
import { LoginService } from "../login.service";
import { AppComponent } from "../app.component";

@Component({
  selector: 'app-my-navbar',
  templateUrl: './my-navbar.component.html',
  styleUrls: ['./my-navbar.component.css']
})
export class MyNavbarComponent implements OnInit {

  loginToken: String = "";


  constructor(public loginService: LoginService) { }

  ngOnInit(): void {
    //this.loginToken = this.loginService.token();
    console.log(this.loginToken)
    //this.loginToken = "true"; // for testing purpose
  }

}
