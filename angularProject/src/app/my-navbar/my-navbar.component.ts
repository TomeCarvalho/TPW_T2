import { Component, OnInit } from '@angular/core';
import { LoginService } from "../login.service";
import {FormBuilder} from "@angular/forms";
import {Router} from "@angular/router";

@Component({
  selector: 'app-my-navbar',
  templateUrl: './my-navbar.component.html',
  styleUrls: ['./my-navbar.component.css']
})
export class MyNavbarComponent implements OnInit {

  loginToken: String = "";

  searchForm = this.formBuilder.group({
    search_prompt: ''
  })

  constructor(public loginService: LoginService, private formBuilder: FormBuilder, private router: Router) { }

  ngOnInit(): void {
    //this.loginToken = this.loginService.token();
    console.log(this.loginToken)
    //this.loginToken = "true"; // for testing purpose
  }

  onSubmit(data: any){
    console.log(data)
    if (data.search_prompt){
      this.router.navigate(['/dashboard'], { queryParams: {'search_prompt': data.search_prompt}})
    }
  }

}
