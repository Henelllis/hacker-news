import React, {Component} from 'react';
import Link from'./Link';
import { Query } from 'react-apollo'
import gql from 'graphql-tag'

const FEED_QUERY = gql`
    query{
      allLinks{
        edges{
          node{
            id,
            createdAt,
            description,
            url
          }
        }
      }
    }
    `
// const FEED_QUERY = gql`
//     {
//       allEmployees {
//         edges {
//           node {
//             id
//             name
//             department {
//               name
//             }
//           }
//         }
//       }
//     }
//     `

class LinkList extends Component{

    render(){


        return(
            <Query query={FEED_QUERY}>
                {({ loading, error, data}) => {
                    if(loading) return<div> LOADING </div>
                    if(error) return <div> ERROR </div>
                    console.log(JSON.stringify(data))
                    let linksToRender = data.allLinks
                    console.log(JSON.stringify(linksToRender))
                    linksToRender = data.allLinks
                    console.log(JSON.stringify(linksToRender.edges))
                    return(
                        <div>
                            {linksToRender.edges.map(link => {
                                console.log('INSIDE MAPPING FUNCTION ' + JSON.stringify(link))
                                return(
                                    <Link key={link.node.id} link={link.node} />
                                )
                            })}
                        </div>
                    )
                }}

            </Query>
        )
    }
}

export default LinkList