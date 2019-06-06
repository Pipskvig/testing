import gql from 'graphql-tag'

const allData = gql`
query {
    allEmployees {
        name,
        companyName,
        positionName,
        hireDate,
        fireDate,
        salary,
        fraction,
        base,
        advance,
        byHours
    }
}`

export {
    allData
}
