<template>
    <v-container grid-list-md text-xs-center>
        <v-layout row wrap>
            <v-flex xs6>
                <h1>Занимаемые должности</h1>
            </v-flex>
            <v-flex xs6>
                <v-container grid-list-md text-xs-center id="search_form">
                    <v-layout row wrap>
                        <v-flex xs12><v-text-field
                                v-model="selector"
                                :counter="200"
                                label="Поиск по сотруднику"
                        ></v-text-field></v-flex>
                        <v-flex xs4><v-checkbox
                                v-model="showFired"
                                label="Показывать уволенных"
                        ></v-checkbox></v-flex>
                        <v-flex xs4><v-btn
                                color="success"
                                @click.stop="neDial=true"
                        >Принять на должность</v-btn></v-flex>
                        <v-flex xs4><v-btn
                                color="error"
                                @click="fireSomePeople()"
                                :disabled="selected.length == 0"
                        >{{ fireText }}</v-btn></v-flex>
                    </v-layout>
                </v-container>
            </v-flex>
            <v-flex xs12>
                <v-data-table
                        v-model="selected"
                        :headers="headers"
                        :items="firedOrNot(showFired)"
                        :search="selector"
                        item-key="name"
                        select-all
                        class="elevation-1"
                >
                    <template v-slot:items="props" >
                        <tr :class="{ 'red': props.item.fireDate }">
                            <td>
                                <v-checkbox
                                        v-model="props.selected"
                                        primary
                                        hide-details
                                        :hidden="isFired(props.item.fireDate)"
                                ></v-checkbox>
                            </td>
                            <td class="text-xs-right">{{ props.item.name }}</td>
                            <td class="text-xs-right">{{ props.item.companyName }}</td>
                            <td class="text-xs-right">{{ props.item.positionName }}</td>
                            <td class="text-xs-right">{{ dateHuman(props.item.hireDate) }}</td>
                            <td class="text-xs-right">{{ dateHuman(props.item.fireDate) }}</td>
                            <td class="text-xs-right" @click.stop="!props.item.fireDate?salDial=true:salDial=false, dialId=props.item.id, sal=props.item.salary, salPer=props.item.fraction">{{ props.item.salary }} ({{ props.item.fraction }}%)</td>
                            <td class="text-xs-right" @click.stop="!props.item.fireDate?baseDial=true:baseDial=false, dialId=props.item.id, salBase=props.item.base">{{ props.item.base }}</td>
                            <td class="text-xs-right" @click.stop="!props.item.fireDate?adDial=true:adDial=false, dialId=props.item.id, adv=props.item.advance">{{ props.item.advance }}</td>
                            <td class="text-xs-right">
                                <v-checkbox
                                        v-model="props.item.byHours"
                                        hide-details
                                        :disabled="isFired(props.item.fireDate)"
                                        @change="switchByHour(props.item.id, props.item.byHours)"
                                ></v-checkbox>
                            </td>
                        </tr>
                    </template>
                    <template v-slot:no-results>
                        <v-alert :value="true" color="error" icon="warning">
                            По запросу "{{ selector }}" результатов не найдено.
                        </v-alert>
                    </template>
                </v-data-table>
                <v-dialog v-model="salDial" max-width="550">
                    <v-card>
                        <v-card-title
                                class="headline grey lighten-2"
                                primary-title
                        >
                            Изменить ставку
                        </v-card-title>
                        <v-card-text>
                            <v-container grid-list-md>
                                <v-layout wrap>
                                    <v-flex xs12 sm6 md4>
                                        <v-text-field v-model="sal" :mask="'#######'" :rules="[()=>!!sal || 'This field is required']" label="Ставка, руб" required></v-text-field>
                                    </v-flex>
                                    <v-flex xs12 sm6 md4>
                                        <v-text-field v-model="salPer" :mask="'###'" :rules="[()=>!!salPer || 'This field is required']" label="Ставка, %" required></v-text-field>
                                    </v-flex>
                                </v-layout>
                            </v-container>
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn
                                    color="error"
                                    flat
                                    @click="salDial = false"
                            >
                                Отменить
                            </v-btn>
                            <v-btn
                                    color="success"
                                    flat
                                    @click="salDial = false; changeSalary();"
                                    :disabled="sal==null && salPer==null"
                            >
                                Сохранить
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
                <v-dialog v-model="baseDial" max-width="550">
                    <v-card>
                        <v-card-title
                                class="headline grey lighten-2"
                                primary-title
                        >
                            Изменить базовую ставку
                        </v-card-title>
                        <v-card-text>
                            <v-container grid-list-md>
                                <v-layout wrap>
                                    <v-flex xs12 sm6 md4>
                                        <v-text-field v-model="salBase" :mask="'#######'" :rules="[()=>!!salBase || 'This field is required']" label="База, руб" required></v-text-field>
                                    </v-flex>
                                </v-layout>
                            </v-container>
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn
                                    color="error"
                                    flat
                                    @click="baseDial = false"
                            >
                                Отменить
                            </v-btn>
                            <v-btn
                                    color="success"
                                    flat
                                    @click="baseDial = false; changeBase();"
                                    :disabled="salBase==null"
                            >
                                Сохранить
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
                <v-dialog v-model="adDial" max-width="550">
                    <v-card>
                        <v-card-title
                                class="headline grey lighten-2"
                                primary-title
                        >
                            Изменить аванс
                        </v-card-title>
                        <v-card-text>
                            <v-container grid-list-md>
                                <v-layout wrap>
                                    <v-flex xs12 sm6 md4>
                                        <v-text-field v-model="adv" :mask="'#######'" :rules="[()=>!!adv || 'This field is required']" label="Аванс, руб" required></v-text-field>
                                    </v-flex>
                                </v-layout>
                            </v-container>
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn
                                    color="error"
                                    flat
                                    @click="adDial = false"
                            >
                                Отменить
                            </v-btn>
                            <v-btn
                                    color="success"
                                    flat
                                    @click="adDial = false; changeAdvance();"
                                    :disabled="adv==null"
                            >
                                Сохранить
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
                <v-dialog v-model="neDial">
                    <v-card>
                        <v-card-title
                                class="headline grey lighten-2"
                                primary-title
                        >
                            Принять работника
                        </v-card-title>
                        <v-card-text>
                            <v-form grid-list-md>
                                <v-layout wrap>
                                    <v-flex xs12 sm6 md4 style="padding: 5px;">
                                        <v-text-field v-model="empName" :rules="[()=>!!empName || 'This field is required']" label="Сотрудник" required></v-text-field>
                                    </v-flex>
                                    <v-flex xs12 sm6 md4 style="padding: 5px;">
                                        <v-text-field v-model="compName" :rules="[()=>!!compName || 'This field is required']" label="Компания" required></v-text-field>
                                    </v-flex>
                                    <v-flex xs12 sm6 md4 style="padding: 5px;">
                                        <v-text-field v-model="pos" :rules="[()=>!!pos || 'This field is required']" label="Должность" required></v-text-field>
                                    </v-flex>
                                    <v-flex xs12 sm6 md4 style="padding: 5px;">
                                        <v-menu
                                                ref="menu"
                                                v-model="menu"
                                                :close-on-content-click="false"
                                                :nudge-right="40"
                                                :return-value.sync="date"
                                                lazy
                                                transition="scale-transition"
                                                offset-y
                                                full-width
                                                min-width="290px"
                                        >
                                            <template v-slot:activator="{ on }">
                                                <v-text-field
                                                        v-model="date"
                                                        :rules="[()=>!!date || 'This field is required']"
                                                        label="Дата приёма"
                                                        prepend-icon="event"
                                                        readonly
                                                        v-on="on"
                                                ></v-text-field>
                                            </template>
                                            <v-date-picker v-model="date" no-title scrollable>
                                                <v-spacer></v-spacer>
                                                <v-btn flat color="primary" @click="menu = false">Cancel</v-btn>
                                                <v-btn flat color="primary" @click="$refs.menu.save(date)">OK</v-btn>
                                            </v-date-picker>
                                        </v-menu>
                                    </v-flex>
                                    <v-flex xs12 sm6 md4 style="padding: 5px;">
                                        <v-text-field v-model="sal" :mask="'#######'" :rules="[()=>!!sal || 'This field is required']" label="Ставка, руб" required></v-text-field>
                                    </v-flex>
                                    <v-flex xs12 sm6 md4 style="padding: 5px;">
                                        <v-text-field v-model="salPer" :mask="'###'" :rules="[()=>!!salPer || 'This field is required']" label="Ставка, %" required></v-text-field>
                                    </v-flex>
                                    <v-flex xs12 sm6 md4 style="padding: 5px;">
                                        <v-text-field v-model="salBase" :mask="'#######'" :rules="[()=>!!salBase || 'This field is required']" label="База" required></v-text-field>
                                    </v-flex>
                                    <v-flex xs12 sm6 md4 style="padding: 5px;">
                                        <v-text-field v-model="adv" :mask="'#######'" :rules="[()=>!!adv || 'This field is required']" label="Аванс, руб" required></v-text-field>
                                    </v-flex>
                                </v-layout>
                            </v-form>
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn
                                    color="error"
                                    flat
                                    @click="neDial = false"
                            >
                                Отменить
                            </v-btn>
                            <v-btn
                                    color="success"
                                    flat
                                    @click="neDial = false; addEmployee();"
                                    :disabled="empName=='' || compName=='' || pos==''
                                    || sal==null || salPer==null || salBase==null || adv==null
                                    || sal=='' || salPer=='' || salBase=='' || adv==''"
                            >
                                Принять
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import gql from 'graphql-tag';

    export default {
        name: 'Employees',
        data () {
            return {
                selected: [],
                selector: "",
                showFired: false,
                salDial: false,
                baseDial:false,
                adDial: false,
                dialId: null,
                neDial: false,
                date: new Date().toISOString().substr(0, 10),
                menu: false,
                modal: false,
                fireText: "Снять с должности",
                empName: "",
                compName: "",
                pos: "",
                sal: null,
                salPer: null,
                salBase: null,
                adv: null,
                headers: [
                    {
                        text: 'Сотрудник',
                        align: 'left',
                        sortable: true,
                        value: 'name'
                    },
                    { text: 'Компания', value: 'companyName' },
                    { text: 'Должность', value: 'positionName' },
                    { text: 'Дата приёма', value: 'hireDate' },
                    { text: 'Дата увольнения', value: 'fireDate' },
                    { text: 'Ставка', value: 'salary' },
                    { text: 'База', value: 'base' },
                    { text: 'Аванс', value: 'advance' },
                    { text: 'Почасовая', value: 'byHours' }
                ]
            }
        },
        apollo: {
            allEmployees: gql`
                query {
                    allEmployees {
                        id
                        name
                        companyName
                        positionName
                        hireDate
                        fireDate
                        salary
                        fraction
                        base
                        advance
                        byHours
                    }
                }`,
            getNotFiredEmployees: gql`
                query {
                    getNotFiredEmployees {
                        id
                        name
                        companyName
                        positionName
                        hireDate
                        fireDate
                        salary
                        fraction
                        base
                        advance
                        byHours
                    }
                }`
        },
        watch: {
            selected: function(val) {
                this.fireText = val.length > 1?'Снять с должностей':'Снять с должности';
                for (var i = 0; i < this.selected.length; i++)
                {
                    if (this.selected[i].fireDate != null)
                        delete this.selected[i];
                }
            }
        },
        methods: {
            addEmployee() {
                const empName = this.empName;
                const compName = this.compName;
                const pos = this.pos;
                const date = this.date;
                const sal = this.sal;
                const salPer = this.salPer;
                const salBase = this.salBase;
                const adv = this.adv;

                this.empName = '';
                this.compName = '';
                this.pos = '';
                this.date = null;
                this.sal = null;
                this.salPer = null;
                this.salBase = null
                this.adv = null;

                this.$apollo.mutate({
                    mutation: gql`
                        mutation($name: String, $companyName: String, $positionName: String, $hireDate: String, $salary: Int, $fraction: Int, $base: Int, $advance: Int, $byHours: Boolean){
                          employeeMutation(name: $name, companyName: $companyName, positionName: $positionName, hireDate: $hireDate, salary: $salary, fraction: $fraction, base: $base, advance: $advance, byHours: $byHours) {
                            employee {
                              name
                              companyName
                              positionName
                              hireDate
                              fireDate
                              salary
                              fraction
                              base
                              advance
                              byHours
                            }
                          }
                        }`,
                    variables: {
                        name: empName,
                        companyName: compName,
                        positionName: pos,
                        hireDate: date,
                        salary: sal,
                        fraction: salPer,
                        base: salBase,
                        advance: adv,
                        byHours: false,
                    }
                }).then(() => {
                    this.$apollo.queries.allEmployees.refetch();
                    this.$apollo.queries.getNotFiredEmployees.refetch();
                });
            },
            changeSalary() {
                const dialId = this.dialId;
                const sal = this.sal;
                const salPer = this.salPer;

                this.dialId = null;
                this.salPer = null;
                this.salBase = null;

                this.$apollo.mutate({
                    mutation: gql`
                        mutation($id: ID, $salary: Int, $fraction: Int){
                          salaryMutation(id: $id, salary: $salary, fraction: $fraction) {
                            employee {
                              id
                              salary
                              fraction
                            }
                          }
                        }`,
                    variables: {
                        id: dialId,
                        salary: sal,
                        fraction: salPer
                    }
                }).then(() => {
                    this.$apollo.queries.allEmployees.refetch();
                    this.$apollo.queries.getNotFiredEmployees.refetch();
                });
            },
            changeBase() {
                const dialId = this.dialId;
                const salBase = this.salBase;

                this.dialId = null;
                this.salBase = null;

                this.$apollo.mutate({
                    mutation: gql`
                        mutation($id: ID, $base: Int){
                          baseMutation(id: $id, base: $base) {
                            employee {
                              id
                              base
                            }
                          }
                        }`,
                    variables: {
                        id: dialId,
                        base: salBase
                    }
                }).then(() => {
                    this.$apollo.queries.allEmployees.refetch();
                    this.$apollo.queries.getNotFiredEmployees.refetch();
                });
            },
            changeAdvance() {
                const dialId = this.dialId;
                const adv = this.adv;

                this.dialId = null;
                this.adv = null;

                this.$apollo.mutate({
                    mutation: gql`
                        mutation($id: ID, $advance: Int){
                          advanceMutation(id: $id, advance: $advance) {
                            employee {
                              id
                              advance
                            }
                          }
                        }`,
                    variables: {
                        id: dialId,
                        advance: adv
                    }
                }).then(() => {
                    this.$apollo.queries.allEmployees.refetch();
                    this.$apollo.queries.getNotFiredEmployees.refetch();
                });
            },
            switchByHour(id, bH) {
                this.$apollo.mutate({
                    mutation: gql`
                        mutation($id: ID, $byHours: Boolean){
                          byHoursSwitchMutation(id: $id, byHours: $byHours) {
                            employee {
                              id
                              byHours
                            }
                          }
                        }`,
                    variables: {
                        id: id,
                        byHours: bH
                    }
                })/*.then(() => {
                    this.$apollo.queries.allEmployees.refetch();
                    this.$apollo.queries.getNotFiredEmployees.refetch();
                })*/;
            },
            fireSomePeople() {
                var id, i;
                for (i = 0; i < this.selected.length; i++) {
                    id = this.selected[i].id;
                    this.$apollo.mutate({
                        mutation: gql`
                            mutation($id: ID){
                              fireMenMutation(id: $id) {
                                employee {
                                  id
                                  fireDate
                                }
                              }
                            }`,
                        variables: {
                            id: id
                        }
                    }).then(() => {
                        this.$apollo.queries.allEmployees.refetch();
                        this.$apollo.queries.getNotFiredEmployees.refetch();
                    });
                }

                this.selected = [];
            },
            firedOrNot(data) {
                return data?this.allEmployees:this.getNotFiredEmployees;
            },
            dateHuman(data) {
                if(data) {
                    var arr = data.split('-');
                    return arr[2].concat('.', arr[1], '.', arr[0]);
                }
                else {
                    return data;
                }
            },
            dateFormal(data) {
                if(data) {
                    var arr = data.split('.');
                    return arr[0].concat('-', arr[1], '-', arr[2]);
                }
                else {
                    return data;
                }
            },
            isFired(data) {
                return data == null || data == "" ? false : true;
            }
        }
    }
</script>

<style>
    .hideCheck {
        display: none;
    }
</style>
