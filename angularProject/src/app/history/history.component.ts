import { Component, OnInit } from '@angular/core';
import {HistoryService} from "../history.service";

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {

  purchasesInfo: any;
  salesInfo: any;

  constructor(private historyService: HistoryService) { }

  ngOnInit(): void {
    this.historyService.getInfo('purchases').subscribe(value => {
      this.purchasesInfo = value
      console.log(value)
    })
    this.historyService.getInfo('sales').subscribe(value => this.purchasesInfo = value)
  }

}
