import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'angularProject';
  isLoggedIn: boolean = false;

  LogIn(){
    this.isLoggedIn = true;
  }

  LogOut(){
    this.isLoggedIn = false;
  }
}
