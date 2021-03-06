import { Component, OnInit } from '@angular/core';
import {HistoryService} from "../history.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {

  purchasesInfo: any;
  salesInfo: any;

  constructor(private historyService: HistoryService, private router: Router) {
    if(localStorage.getItem('loginToken') == ''){
      router.navigate(['dashboard'])
    }
  }

  ngOnInit(): void {
    this.historyService.getInfo('purchases').subscribe(value => {
      this.purchasesInfo = value
      console.log(value)
    })
    this.historyService.getInfo('sales').subscribe(value => {
      this.salesInfo = value
      console.log(value)
    })
  }

}
